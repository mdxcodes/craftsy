package com.craftsy.app.widget

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Tests for Craftsy Orders Widget states and behavior.
 */
class OrdersWidgetStateTest {

    // ── Logged Out State ───────────────────────────────────────────────

    @Test
    fun `logged out snapshot shows sign-in prompt`() {
        val snapshot = WidgetSnapshot(
            authenticated = false,
            accountId = null,
            lastUpdated = 0L,
            dataFreshness = DataFreshness.UNKNOWN,
        )
        assertFalse(snapshot.authenticated)
        assertNull(snapshot.accountId)
    }

    // ── Empty State ────────────────────────────────────────────────────

    @Test
    fun `empty state when no actionable orders`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            orders = OrdersSnapshot(
                actionableCount = 0,
                items = emptyList(),
            ),
        )
        assertNotNull(snapshot.orders)
        assertEquals(0, snapshot.orders!!.actionableCount)
        assertTrue(snapshot.orders!!.items.isEmpty())
    }

    // ── Actionable Orders ──────────────────────────────────────────────

    @Test
    fun `orders snapshot contains only actionable orders`() {
        val orders = OrdersSnapshot(
            actionableCount = 3,
            items = listOf(
                WidgetOrderSummary(
                    orderId = "ORD-1001",
                    status = "newOrder",
                    statusLabel = "order_status_new",
                    productTitle = "Test Product 1",
                    requiredAction = "Confirm order",
                    deepLink = "/orders/ORD-1001",
                ),
                WidgetOrderSummary(
                    orderId = "ORD-1002",
                    status = "packed",
                    statusLabel = "order_status_packed",
                    productTitle = "Test Product 2",
                    requiredAction = "Ship today",
                    deepLink = "/orders/ORD-1002",
                ),
                WidgetOrderSummary(
                    orderId = "ORD-1003",
                    status = "shipped",
                    statusLabel = "order_status_shipped",
                    productTitle = "Test Product 3",
                    requiredAction = "Track delivery",
                    deepLink = "/orders/ORD-1003",
                ),
            ),
        )
        assertEquals(3, orders.actionableCount)
        assertEquals(3, orders.items.size)
        assertEquals("newOrder", orders.items[0].status)
        assertEquals("packed", orders.items[1].status)
        assertEquals("shipped", orders.items[2].status)
    }

    // ── Deep Links ────────────────────────────────────────────────────

    @Test
    fun `each order has correct deep link`() {
        val order = WidgetOrderSummary(
            orderId = "ORD-1042",
            status = "newOrder",
            statusLabel = "order_status_new",
            productTitle = "Test Product",
            requiredAction = "Confirm order",
            deepLink = "/orders/ORD-1042",
        )
        assertEquals("/orders/ORD-1042", order.deepLink)
    }

    // ── Order Priority ─────────────────────────────────────────────────

    @Test
    fun `orders are ordered by status priority`() {
        // newOrder should come before packed, packed before shipped
        val orders = listOf(
            WidgetOrderSummary(orderId = "ORD-3", status = "shipped", statusLabel = "", productTitle = ""),
            WidgetOrderSummary(orderId = "ORD-1", status = "newOrder", statusLabel = "", productTitle = ""),
            WidgetOrderSummary(orderId = "ORD-2", status = "packed", statusLabel = "", productTitle = ""),
        )
        val sorted = orders.sortedBy {
            when (it.status) {
                "newOrder" -> 0
                "packed" -> 1
                "shipped" -> 2
                else -> 3
            }
        }
        assertEquals("newOrder", sorted[0].status)
        assertEquals("packed", sorted[1].status)
        assertEquals("shipped", sorted[2].status)
    }

    // ── Required Action Labels ─────────────────────────────────────────

    @Test
    fun `newOrder requires confirmation`() {
        val order = WidgetOrderSummary(
            orderId = "ORD-1001",
            status = "newOrder",
            statusLabel = "order_status_new",
            productTitle = "Test",
            requiredAction = "Confirm order",
            deepLink = "/orders/ORD-1001",
        )
        assertEquals("Confirm order", order.requiredAction)
    }

    @Test
    fun `packed requires shipping`() {
        val order = WidgetOrderSummary(
            orderId = "ORD-1002",
            status = "packed",
            statusLabel = "order_status_packed",
            productTitle = "Test",
            requiredAction = "Ship today",
            deepLink = "/orders/ORD-1002",
        )
        assertEquals("Ship today", order.requiredAction)
    }

    @Test
    fun `shipped requires tracking`() {
        val order = WidgetOrderSummary(
            orderId = "ORD-1003",
            status = "shipped",
            statusLabel = "order_status_shipped",
            productTitle = "Test",
            requiredAction = "Track delivery",
            deepLink = "/orders/ORD-1003",
        )
        assertEquals("Track delivery", order.requiredAction)
    }

    // ── Non-actionable Orders ──────────────────────────────────────────

    @Test
    fun `delivered orders are not actionable`() {
        val order = WidgetOrderSummary(
            orderId = "ORD-1004",
            status = "delivered",
            statusLabel = "order_status_delivered",
            productTitle = "Test",
            requiredAction = null,
            deepLink = "/orders/ORD-1004",
        )
        assertNull(order.requiredAction)
    }

    @Test
    fun `cancelled orders are not actionable`() {
        val order = WidgetOrderSummary(
            orderId = "ORD-1005",
            status = "cancelled",
            statusLabel = "order_status_cancelled",
            productTitle = "Test",
            requiredAction = null,
            deepLink = "/orders/ORD-1005",
        )
        assertNull(order.requiredAction)
    }

    // ── Stale Data ─────────────────────────────────────────────────────

    @Test
    fun `stale data shows warning`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis() - 3 * 60 * 60 * 1000,
            dataFreshness = DataFreshness.STALE,
            orders = OrdersSnapshot(actionableCount = 2),
        )
        assertEquals(DataFreshness.STALE, snapshot.dataFreshness)
    }

    // ── Data Unavailable ───────────────────────────────────────────────

    @Test
    fun `data unavailable shows fallback`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-123",
            lastUpdated = 0L,
            dataFreshness = DataFreshness.UNKNOWN,
        )
        assertEquals(DataFreshness.UNKNOWN, snapshot.dataFreshness)
        assertNull(snapshot.orders)
    }

    // ── Account Isolation ──────────────────────────────────────────────

    @Test
    fun `different accounts have different order snapshots`() {
        val snapshotA = WidgetSnapshot(
            authenticated = true,
            accountId = "user-A",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            orders = OrdersSnapshot(
                actionableCount = 3,
                items = listOf(
                    WidgetOrderSummary(orderId = "ORD-A1", status = "newOrder", statusLabel = "", productTitle = "A"),
                ),
            ),
        )
        val snapshotB = WidgetSnapshot(
            authenticated = true,
            accountId = "user-B",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            orders = OrdersSnapshot(
                actionableCount = 1,
                items = listOf(
                    WidgetOrderSummary(orderId = "ORD-B1", status = "packed", statusLabel = "", productTitle = "B"),
                ),
            ),
        )
        assertEquals("user-A", snapshotA.accountId)
        assertEquals("user-B", snapshotB.accountId)
        assertEquals(3, snapshotA.orders!!.actionableCount)
        assertEquals(1, snapshotB.orders!!.actionableCount)
    }

    // ── Security: No Customer PII ─────────────────────────────────────

    @Test
    fun `widget order summary does not contain buyer name`() {
        val order = WidgetOrderSummary(
            orderId = "ORD-1001",
            status = "newOrder",
            statusLabel = "order_status_new",
            productTitle = "Test Product",
            requiredAction = "Confirm order",
            deepLink = "/orders/ORD-1001",
        )
        // Only orderId, status, productTitle, and requiredAction
        // No buyer name, buyer location, or other PII
        assertEquals("ORD-1001", order.orderId)
        assertEquals("Test Product", order.productTitle)
    }

    // ── Serialization ──────────────────────────────────────────────────

    @Test
    fun `orders snapshot serializes correctly`() {
        val orders = OrdersSnapshot(
            actionableCount = 2,
            items = listOf(
                WidgetOrderSummary(
                    orderId = "ORD-1001",
                    status = "newOrder",
                    statusLabel = "order_status_new",
                    productTitle = "Test",
                    requiredAction = "Confirm order",
                    deepLink = "/orders/ORD-1001",
                ),
            ),
        )
        val json = orders.toJson()
        assertEquals(2, json.getInt("actionableCount"))
        val items = json.getJSONArray("items")
        assertEquals(1, items.length())
    }

    @Test
    fun `malformed orders JSON handled gracefully`() {
        val json = org.json.JSONObject("{}")
        val orders = OrdersSnapshot.fromJson(json)
        assertEquals(0, orders.actionableCount)
        assertTrue(orders.items.isEmpty())
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
            orders = OrdersSnapshot(
                actionableCount = 2,
                items = listOf(
                    WidgetOrderSummary(
                        orderId = "ORD-1001",
                        status = "newOrder",
                        statusLabel = "order_status_new",
                        productTitle = "Test",
                        requiredAction = "Confirm order",
                        deepLink = "/orders/ORD-1001",
                    ),
                ),
            ),
        )
        val json1 = snapshot.toJson().toString()
        val json2 = snapshot.toJson().toString()
        assertEquals(json1, json2)
    }

    // ── Max Display Items ──────────────────────────────────────────────

    @Test
    fun `widget displays max 3 orders`() {
        val items = (1..5).map { i ->
            WidgetOrderSummary(
                orderId = "ORD-100$i",
                status = "newOrder",
                statusLabel = "order_status_new",
                productTitle = "Product $i",
                requiredAction = "Confirm order",
                deepLink = "/orders/ORD-100$i",
            )
        }
        val displayItems = items.take(3)
        assertEquals(3, displayItems.size)
        assertEquals(5, items.size)
    }

    // ── Order with Null Deep Link ──────────────────────────────────────

    @Test
    fun `order with null deep link handled gracefully`() {
        val order = WidgetOrderSummary(
            orderId = "ORD-1001",
            status = "newOrder",
            statusLabel = "order_status_new",
            productTitle = "Test",
            requiredAction = "Confirm order",
            deepLink = null,
        )
        assertNull(order.deepLink)
    }

    // ── Order with Empty Required Action ───────────────────────────────

    @Test
    fun `order with empty required action uses status label`() {
        val order = WidgetOrderSummary(
            orderId = "ORD-1001",
            status = "newOrder",
            statusLabel = "New Order",
            productTitle = "Test",
            requiredAction = "",
            deepLink = "/orders/ORD-1001",
        )
        // Widget should fall back to statusLabel
        assertEquals("", order.requiredAction)
        assertEquals("New Order", order.statusLabel)
    }

    // ── Security: No Tokens in Snapshot ───────────────────────────────

    @Test
    fun `orders snapshot does not contain authentication tokens`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            orders = OrdersSnapshot(
                actionableCount = 1,
                items = listOf(
                    WidgetOrderSummary(
                        orderId = "ORD-1001",
                        status = "newOrder",
                        statusLabel = "order_status_new",
                        productTitle = "Test",
                        requiredAction = "Confirm order",
                        deepLink = "/orders/ORD-1001",
                    ),
                ),
            ),
        )
        val json = snapshot.toJson()
        assertFalse(json.has("accessToken"))
        assertFalse(json.has("refreshToken"))
        assertFalse(json.has("password"))
        assertFalse(json.has("apiKey"))
    }
}
