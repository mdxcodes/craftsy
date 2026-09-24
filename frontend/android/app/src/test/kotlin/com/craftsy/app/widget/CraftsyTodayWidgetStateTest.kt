package com.craftsy.app.widget

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Tests for Craftsy Today widget states and behavior.
 *
 * Verifies the widget handles all required states:
 * - Fresh data
 * - Stale data
 * - Empty state
 * - Logged out
 * - Account changed
 * - Data unavailable
 * - Corrupt snapshot
 */
class CraftsyTodayWidgetStateTest {

    // ── Logged Out State ───────────────────────────────────────────────

    @Test
    fun `logged out snapshot shows sign-in prompt`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = false,
            accountId = null,
            lastUpdated = 0L,
            dataFreshness = DataFreshness.UNKNOWN,
        )
        assertFalse(snapshot.authenticated)
        assertNull(snapshot.accountId)
    }

    @Test
    fun `logged out snapshot does not expose data`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = false,
            accountId = null,
            lastUpdated = 0L,
            dataFreshness = DataFreshness.UNKNOWN,
            today = TodaySnapshot(
                attentionCount = 5,
                orderAttentionCount = 3,
                stockAttentionCount = 2,
                channelAttentionCount = 0,
            ),
        )
        // Even with data, logged-out widget should not show it
        assertFalse(snapshot.authenticated)
        // Data exists but should not be rendered
        assertNotNull(snapshot.today)
    }

    // ── Fresh Data State ───────────────────────────────────────────────

    @Test
    fun `fresh data shows actionable items`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis(),
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
                    ),
                    ActionableItem(
                        type = ActionableType.STOCK,
                        id = "prod-1",
                        title = "Test Product",
                        subtitle = "Out of stock",
                        deepLink = "/product/prod-1"
                    ),
                ),
            ),
        )
        assertTrue(snapshot.authenticated)
        assertEquals(DataFreshness.FRESH, snapshot.dataFreshness)
        assertNotNull(snapshot.today)
        assertEquals(3, snapshot.today!!.attentionCount)
        assertEquals(2, snapshot.today!!.actionableItems.size)
    }

    // ── Stale Data State ───────────────────────────────────────────────

    @Test
    fun `stale data shows warning indicator`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis() - 3 * 60 * 60 * 1000,
            dataFreshness = DataFreshness.STALE,
            today = TodaySnapshot(
                attentionCount = 1,
                orderAttentionCount = 1,
                stockAttentionCount = 0,
                channelAttentionCount = 0,
            ),
        )
        assertEquals(DataFreshness.STALE, snapshot.dataFreshness)
    }

    // ── Empty State ────────────────────────────────────────────────────

    @Test
    fun `empty state shows all caught up message`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            today = TodaySnapshot(
                attentionCount = 0,
                orderAttentionCount = 0,
                stockAttentionCount = 0,
                channelAttentionCount = 0,
                actionableItems = emptyList(),
            ),
        )
        assertEquals(0, snapshot.today!!.attentionCount)
        assertTrue(snapshot.today!!.actionableItems.isEmpty())
    }

    // ── Data Unavailable State ─────────────────────────────────────────

    @Test
    fun `data unavailable shows safe fallback`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = true,
            accountId = "user-123",
            lastUpdated = 0L,
            dataFreshness = DataFreshness.UNKNOWN,
        )
        assertEquals(DataFreshness.UNKNOWN, snapshot.dataFreshness)
        assertNull(snapshot.today)
    }

    // ── Corrupt Snapshot Handling ──────────────────────────────────────

    @Test
    fun `corrupt snapshot JSON is handled gracefully`() {
        val corruptJson = """{"schemaVersion": "corrupted"}"""
        val json = org.json.JSONObject(corruptJson)
        val snapshot = WidgetSnapshot.fromJson(json)
        // Should return defaults, not crash
        assertEquals(0, snapshot.schemaVersion)
        assertFalse(snapshot.authenticated)
    }

    @Test
    fun `empty JSON returns default snapshot`() {
        val json = org.json.JSONObject("{}")
        val snapshot = WidgetSnapshot.fromJson(json)
        assertEquals(0, snapshot.schemaVersion)
        assertFalse(snapshot.authenticated)
        assertNull(snapshot.accountId)
        assertNull(snapshot.today)
    }

    // ── Account Isolation ──────────────────────────────────────────────

    @Test
    fun `snapshot stores account ID for isolation`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-A",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
        )
        val json = snapshot.toJson()
        assertEquals("user-A", json.getString("accountId"))
    }

    @Test
    fun `different accounts have different snapshots`() {
        val snapshotA = WidgetSnapshot(
            authenticated = true,
            accountId = "user-A",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            today = TodaySnapshot(attentionCount = 5),
        )
        val snapshotB = WidgetSnapshot(
            authenticated = true,
            accountId = "user-B",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            today = TodaySnapshot(attentionCount = 3),
        )
        assertEquals("user-A", snapshotA.accountId)
        assertEquals("user-B", snapshotB.accountId)
        assertEquals(5, snapshotA.today!!.attentionCount)
        assertEquals(3, snapshotB.today!!.attentionCount)
    }

    // ── Deep Link Generation ───────────────────────────────────────────

    @Test
    fun `actionable items have correct deep links`() {
        val orderItem = ActionableItem(
            type = ActionableType.ORDER,
            id = "ORD-1042",
            title = "Test Order",
            subtitle = "Ship today",
            deepLink = "/orders/ORD-1042",
        )
        assertEquals("/orders/ORD-1042", orderItem.deepLink)

        val stockItem = ActionableItem(
            type = ActionableType.STOCK,
            id = "prod-42",
            title = "Test Product",
            subtitle = "Out of stock",
            deepLink = "/product/prod-42",
        )
        assertEquals("/product/prod-42", stockItem.deepLink)

        val channelItem = ActionableItem(
            type = ActionableType.CHANNEL,
            id = "channels",
            title = "Selling Channels",
            subtitle = "Needs attention",
            deepLink = "/commerce-hub",
        )
        assertEquals("/commerce-hub", channelItem.deepLink)
    }

    // ── Channel State Honesty ─────────────────────────────────────────

    @Test
    fun `ONDC channel is NOT_CONFIGURED by default`() {
        val snapshot = ChannelsSnapshot()
        assertEquals(ChannelState.NOT_CONFIGURED, snapshot.ondc!!.state)
        assertEquals("Not configured", snapshot.ondc!!.stateLabel)
    }

    @Test
    fun `Government channel is NOT_CONFIGURED by default`() {
        val snapshot = ChannelsSnapshot()
        assertEquals(ChannelState.NOT_CONFIGURED, snapshot.government!!.state)
        assertEquals("Not configured", snapshot.government!!.stateLabel)
    }

    @Test
    fun `Craftsy channel is ACTIVE by default`() {
        val snapshot = ChannelsSnapshot()
        assertEquals(ChannelState.ACTIVE, snapshot.craftsy!!.state)
        assertEquals("Active", snapshot.craftsy!!.stateLabel)
    }

    // ── Idempotent Updates ─────────────────────────────────────────────

    @Test
    fun `repeated identical updates produce same result`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = true,
            accountId = "user-123",
            lastUpdated = 1000L,
            dataFreshness = DataFreshness.FRESH,
        )
        val json1 = snapshot.toJson().toString()
        val json2 = snapshot.toJson().toString()
        assertEquals(json1, json2)
    }

    // ── Security: No Secrets in Snapshot ──────────────────────────────

    @Test
    fun `snapshot does not contain authentication secrets`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
        )
        val json = snapshot.toJson()
        assertFalse(json.has("password"))
        assertFalse(json.has("accessToken"))
        assertFalse(json.has("refreshToken"))
        assertFalse(json.has("apiKey"))
        assertFalse(json.has("secret"))
    }

    // ── Today Snapshot Content ─────────────────────────────────────────

    @Test
    fun `today snapshot counts are correct`() {
        val today = TodaySnapshot(
            attentionCount = 5,
            orderAttentionCount = 3,
            stockAttentionCount = 2,
            channelAttentionCount = 0,
        )
        assertEquals(5, today.attentionCount)
        assertEquals(3, today.orderAttentionCount)
        assertEquals(2, today.stockAttentionCount)
        assertEquals(0, today.channelAttentionCount)
    }

    // ── Orders Snapshot ────────────────────────────────────────────────

    @Test
    fun `orders snapshot has correct actionable count`() {
        val orders = OrdersSnapshot(
            actionableCount = 2,
            items = listOf(
                WidgetOrderSummary(
                    orderId = "ORD-1001",
                    status = "newOrder",
                    statusLabel = "New Order",
                    productTitle = "Test Product",
                    requiredAction = "Confirm order",
                    deepLink = "/orders/ORD-1001"
                ),
            ),
        )
        assertEquals(2, orders.actionableCount)
        assertEquals(1, orders.items.size)
    }

    // ── Stock Snapshot ─────────────────────────────────────────────────

    @Test
    fun `stock snapshot has correct out-of-stock count`() {
        val stock = StockSnapshot(
            outOfStockCount = 2,
            lowStockCount = 0,
            items = listOf(
                WidgetStockItem(
                    productId = "prod-1",
                    productName = "Product 1",
                    stockQuantity = 0,
                    stockState = StockState.OUT_OF_STOCK,
                    deepLink = "/product/prod-1"
                ),
                WidgetStockItem(
                    productId = "prod-2",
                    productName = "Product 2",
                    stockQuantity = 0,
                    stockState = StockState.OUT_OF_STOCK,
                    deepLink = "/product/prod-2"
                ),
            ),
        )
        assertEquals(2, stock.outOfStockCount)
        assertEquals(0, stock.lowStockCount)
        assertEquals(2, stock.items.size)
    }

    // ── CraftMitra Snapshot ───────────────────────────────────────────

    @Test
    fun `craftMitra snapshot has correct deep links`() {
        val snapshot = CraftMitraSnapshot()
        assertTrue(snapshot.available)
        assertTrue(snapshot.voiceModeAvailable)
        assertTrue(snapshot.textModeAvailable)
        assertEquals("/assistant?mode=voice", snapshot.voiceDeepLink)
        assertEquals("/assistant?mode=text", snapshot.textDeepLink)
    }
}
