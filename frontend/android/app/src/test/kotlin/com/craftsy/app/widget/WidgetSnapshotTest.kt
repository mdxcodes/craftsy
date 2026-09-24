package com.craftsy.app.widget

import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Unit tests for widget snapshot serialization, projection, and data handling.
 *
 * These tests verify the core data bridge between Flutter and Android
 * without requiring a running Flutter engine or Android system service.
 */
class WidgetSnapshotTest {

    // ── Snapshot Serialization ─────────────────────────────────────────

    @Test
    fun `snapshot serializes to JSON and back`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = true,
            accountId = "user-123",
            lastUpdated = 1000L,
            dataFreshness = DataFreshness.FRESH,
            today = TodaySnapshot(
                attentionCount = 3,
                orderAttentionCount = 2,
                stockAttentionCount = 1,
                channelAttentionCount = 0,
                actionableItems = listOf(
                    ActionableItem(
                        type = ActionableType.ORDER,
                        id = "ORD-1001",
                        title = "Test Order",
                        subtitle = "Ship today",
                        deepLink = "/orders/ORD-1001"
                    )
                )
            ),
            orders = OrdersSnapshot(
                actionableCount = 1,
                items = listOf(
                    WidgetOrderSummary(
                        orderId = "ORD-1001",
                        status = "newOrder",
                        statusLabel = "New Order",
                        productTitle = "Test Product",
                        requiredAction = "Confirm order",
                        deepLink = "/orders/ORD-1001"
                    )
                )
            ),
            stock = StockSnapshot(
                outOfStockCount = 1,
                lowStockCount = 0,
                items = listOf(
                    WidgetStockItem(
                        productId = "prod-1",
                        productName = "Test Product",
                        stockQuantity = 0,
                        stockState = StockState.OUT_OF_STOCK,
                        deepLink = "/product/prod-1"
                    )
                )
            ),
            channels = ChannelsSnapshot(
                craftsy = ChannelStatus(
                    channelName = "Craftsy",
                    state = ChannelState.ACTIVE,
                    stateLabel = "Active",
                    deepLink = "/catalogue"
                ),
                ondc = ChannelStatus(
                    channelName = "ONDC",
                    state = ChannelState.NOT_CONFIGURED,
                    stateLabel = "Not configured"
                ),
                government = ChannelStatus(
                    channelName = "Government",
                    state = ChannelState.NOT_CONFIGURED,
                    stateLabel = "Not configured"
                )
            ),
            craftMitra = CraftMitraSnapshot(
                available = true,
                voiceModeAvailable = true,
                textModeAvailable = true
            )
        )

        // Serialize
        val json = snapshot.toJson()
        assertEquals(1, json.getInt("schemaVersion"))
        assertTrue(json.getBoolean("authenticated"))
        assertEquals("user-123", json.getString("accountId"))
        assertEquals(1000L, json.getLong("lastUpdated"))
        assertEquals("FRESH", json.getString("dataFreshness"))

        // Deserialize
        val restored = WidgetSnapshot.fromJson(json)
        assertEquals(snapshot.schemaVersion, restored.schemaVersion)
        assertEquals(snapshot.authenticated, restored.authenticated)
        assertEquals(snapshot.accountId, restored.accountId)
        assertEquals(snapshot.lastUpdated, restored.lastUpdated)
        assertEquals(snapshot.dataFreshness, restored.dataFreshness)

        // Verify nested objects
        assertNotNull(restored.today)
        assertEquals(3, restored.today!!.attentionCount)
        assertEquals(1, restored.today!!.actionableItems.size)
        assertEquals("ORD-1001", restored.today!!.actionableItems[0].id)

        assertNotNull(restored.orders)
        assertEquals(1, restored.orders!!.actionableCount)
        assertEquals("ORD-1001", restored.orders!!.items[0].orderId)

        assertNotNull(restored.stock)
        assertEquals(1, restored.stock!!.outOfStockCount)
        assertEquals(StockState.OUT_OF_STOCK, restored.stock!!.items[0].stockState)

        assertNotNull(restored.channels)
        assertEquals(ChannelState.ACTIVE, restored.channels!!.craftsy!!.state)
        assertEquals(ChannelState.NOT_CONFIGURED, restored.channels!!.ondc!!.state)
        assertEquals(ChannelState.NOT_CONFIGURED, restored.channels!!.government!!.state)

        assertNotNull(restored.craftMitra)
        assertTrue(restored.craftMitra!!.available)
    }

    @Test
    fun `snapshot handles null optional fields`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = false,
            lastUpdated = 0L,
            dataFreshness = DataFreshness.UNKNOWN
        )

        val json = snapshot.toJson()
        val restored = WidgetSnapshot.fromJson(json)

        assertFalse(restored.authenticated)
        assertNull(restored.accountId)
        assertNull(restored.today)
        assertNull(restored.orders)
        assertNull(restored.stock)
        assertNull(restored.channels)
        assertNull(restored.craftMitra)
    }

    @Test
    fun `snapshot schema version is 1`() {
        assertEquals(1, WidgetSnapshot.CURRENT_SCHEMA_VERSION)
    }

    // ── Data Freshness ─────────────────────────────────────────────────

    @Test
    fun `data freshness enum has expected values`() {
        assertEquals(4, DataFreshness.values().size)
        assertNotNull(DataFreshness.valueOf("FRESH"))
        assertNotNull(DataFreshness.valueOf("STALE"))
        assertNotNull(DataFreshness.valueOf("EXPIRED"))
        assertNotNull(DataFreshness.valueOf("UNKNOWN"))
    }

    // ── Stock State ────────────────────────────────────────────────────

    @Test
    fun `stock state enum has expected values`() {
        assertEquals(3, StockState.values().size)
        assertNotNull(StockState.valueOf("IN_STOCK"))
        assertNotNull(StockState.valueOf("LOW"))
        assertNotNull(StockState.valueOf("OUT_OF_STOCK"))
    }

    // ── Channel State ──────────────────────────────────────────────────

    @Test
    fun `channel state enum has expected values``() {
        assertEquals(8, ChannelState.values().size)
        assertNotNull(ChannelState.valueOf("ACTIVE"))
        assertNotNull(ChannelState.valueOf("READY"))
        assertNotNull(ChannelState.valueOf("NEEDS_ATTENTION"))
        assertNotNull(ChannelState.valueOf("NOT_CONFIGURED"))
        assertNotNull(ChannelState.valueOf("UPDATING"))
        assertNotNull(ChannelState.valueOf("UNAVAILABLE"))
        assertNotNull(ChannelState.valueOf("ERROR"))
        assertNotNull(ChannelState.valueOf("PREPARATION_NEEDED"))
    }

    // ── Actionable Type ────────────────────────────────────────────────

    @Test
    fun `actionable type enum has expected values`() {
        assertEquals(3, ActionableType.values().size)
        assertNotNull(ActionableType.valueOf("ORDER"))
        assertNotNull(ActionableType.valueOf("STOCK"))
        assertNotNull(ActionableType.valueOf("CHANNEL"))
    }

    // ── Malformed Data Handling ────────────────────────────────────────

    @Test
    fun `fromJson handles malformed JSON gracefully`() {
        val malformedJson = """{"schemaVersion": "not-a-number"}"""
        val json = JSONObject(malformedJson)
        val snapshot = WidgetSnapshot.fromJson(json)
        // Should not crash, should return defaults
        assertEquals(0, snapshot.schemaVersion)
        assertFalse(snapshot.authenticated)
    }

    @Test
    fun `fromJson handles empty JSON`() {
        val json = JSONObject("{}")
        val snapshot = WidgetSnapshot.fromJson(json)
        assertEquals(0, snapshot.schemaVersion)
        assertFalse(snapshot.authenticated)
        assertNull(snapshot.accountId)
    }

    @Test
    fun `fromJson handles missing fields`() {
        val json = JSONObject("""{"schemaVersion": 1, "authenticated": true}""")
        val snapshot = WidgetSnapshot.fromJson(json)
        assertEquals(1, snapshot.schemaVersion)
        assertTrue(snapshot.authenticated)
        assertNull(snapshot.today)
        assertNull(snapshot.orders)
    }

    // ── Deep Link Generation ───────────────────────────────────────────

    @Test
    fun `order summary generates correct deep link`() {
        val order = WidgetOrderSummary(
            orderId = "ORD-1042",
            status = "newOrder",
            statusLabel = "New Order",
            productTitle = "Blue Pottery Vase",
            requiredAction = "Confirm order",
            deepLink = "/orders/ORD-1042"
        )
        assertEquals("/orders/ORD-1042", order.deepLink)
    }

    @Test
    fun `stock item generates correct deep link`() {
        val item = WidgetStockItem(
            productId = "prod-42",
            productName = "Wooden Lamp",
            stockQuantity = 0,
            stockState = StockState.OUT_OF_STOCK,
            deepLink = "/product/prod-42"
        )
        assertEquals("/product/prod-42", item.deepLink)
    }

    @Test
    fun `craftMitra snapshot has correct deep links`() {
        val snapshot = CraftMitraSnapshot()
        assertEquals("/assistant?mode=voice", snapshot.voiceDeepLink)
        assertEquals("/assistant?mode=text", snapshot.textDeepLink)
    }

    // ── Channel Status Honesty ─────────────────────────────────────────

    @Test
    fun `channel status defaults to NOT_CONFIGURED for ONDC`() {
        val snapshot = ChannelsSnapshot()
        assertEquals(ChannelState.NOT_CONFIGURED, snapshot.ondc!!.state)
        assertEquals("Not configured", snapshot.ondc!!.stateLabel)
    }

    @Test
    fun `channel status defaults to NOT_CONFIGURED for Government`() {
        val snapshot = ChannelsSnapshot()
        assertEquals(ChannelState.NOT_CONFIGURED, snapshot.government!!.state)
        assertEquals("Not configured", snapshot.government!!.stateLabel)
    }

    @Test
    fun `channel status defaults to ACTIVE for Craftsy`() {
        val snapshot = ChannelsSnapshot()
        assertEquals(ChannelState.ACTIVE, snapshot.craftsy!!.state)
        assertEquals("Active", snapshot.craftsy!!.stateLabel)
    }

    // ── Idempotent Updates ─────────────────────────────────────────────

    @Test
    fun `same snapshot produces same JSON`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = true,
            accountId = "user-123",
            lastUpdated = 1000L,
            dataFreshness = DataFreshness.FRESH
        )

        val json1 = snapshot.toJson().toString()
        val json2 = snapshot.toJson().toString()
        assertEquals(json1, json2)
    }

    // ── Account Isolation ──────────────────────────────────────────────

    @Test
    fun `snapshot stores account ID for isolation`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-456"
        )
        val json = snapshot.toJson()
        assertEquals("user-456", json.getString("accountId"))
    }

    @Test
    fun `snapshot handles null account ID for logged-out state`() {
        val snapshot = WidgetSnapshot(
            authenticated = false,
            accountId = null
        )
        val json = snapshot.toJson()
        assertTrue(json.isNull("accountId"))
    }
}
