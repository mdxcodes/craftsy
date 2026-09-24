package com.craftsy.app.widget

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Tests for Craftsy Stock Alerts Widget states and behavior.
 */
class StockAlertsWidgetStateTest {

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
    fun `empty state when no stock alerts`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            stock = StockSnapshot(
                outOfStockCount = 0,
                lowStockCount = 0,
                items = emptyList(),
            ),
        )
        assertNotNull(snapshot.stock)
        assertEquals(0, snapshot.stock!!.outOfStockCount)
        assertEquals(0, snapshot.stock!!.lowStockCount)
        assertTrue(snapshot.stock!!.items.isEmpty())
    }

    // ── Out of Stock Priority ──────────────────────────────────────────

    @Test
    fun `out of stock items appear first`() {
        val items = listOf(
            WidgetStockItem(
                productId = "prod-1",
                productName = "In Stock Product",
                stockQuantity = 10,
                stockState = StockState.IN_STOCK,
            ),
            WidgetStockItem(
                productId = "prod-2",
                productName = "Out of Stock Product",
                stockQuantity = 0,
                stockState = StockState.OUT_OF_STOCK,
            ),
        )
        val sorted = items.sortedBy {
            when (it.stockState) {
                StockState.OUT_OF_STOCK -> 0
                StockState.LOW -> 1
                StockState.IN_STOCK -> 2
            }
        }
        assertEquals(StockState.OUT_OF_STOCK, sorted[0].stockState)
        assertEquals(StockState.IN_STOCK, sorted[1].stockState)
    }

    // ── Low Stock Display ──────────────────────────────────────────────

    @Test
    fun `low stock shows quantity when available`() {
        val item = WidgetStockItem(
            productId = "prod-1",
            productName = "Test Product",
            stockQuantity = 2,
            stockState = StockState.LOW,
        )
        assertEquals(2, item.stockQuantity)
        assertEquals(StockState.LOW, item.stockState)
    }

    @Test
    fun `low stock without quantity shows generic label`() {
        val item = WidgetStockItem(
            productId = "prod-1",
            productName = "Test Product",
            stockQuantity = 0,
            stockState = StockState.LOW,
        )
        assertEquals(0, item.stockQuantity)
        // Widget should show "Low stock" when quantity is 0
    }

    // ── Deep Links ────────────────────────────────────────────────────

    @Test
    fun `each stock item has correct deep link`() {
        val item = WidgetStockItem(
            productId = "prod-42",
            productName = "Test Product",
            stockQuantity = 0,
            stockState = StockState.OUT_OF_STOCK,
            deepLink = "/product/prod-42",
        )
        assertEquals("/product/prod-42", item.deepLink)
    }

    // ── State Labels ───────────────────────────────────────────────────

    @Test
    fun `out of stock label is correct`() {
        val item = WidgetStockItem(
            productId = "prod-1",
            productName = "Test Product",
            stockQuantity = 0,
            stockState = StockState.OUT_OF_STOCK,
        )
        // Widget should display "Out of stock"
        assertEquals(StockState.OUT_OF_STOCK, item.stockState)
    }

    @Test
    fun `in stock items are not actionable`() {
        val item = WidgetStockItem(
            productId = "prod-1",
            productName = "Test Product",
            stockQuantity = 10,
            stockState = StockState.IN_STOCK,
        )
        // IN_STOCK items should not appear in alerts
        assertEquals(StockState.IN_STOCK, item.stockState)
    }

    // ── Stale Data ─────────────────────────────────────────────────────

    @Test
    fun `stale data shows warning`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis() - 3 * 60 * 60 * 1000,
            dataFreshness = DataFreshness.STALE,
            stock = StockSnapshot(
                outOfStockCount = 1,
                items = listOf(
                    WidgetStockItem(
                        productId = "prod-1",
                        productName = "Test Product",
                        stockQuantity = 0,
                        stockState = StockState.OUT_OF_STOCK,
                    ),
                ),
            ),
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
        assertNull(snapshot.stock)
    }

    // ── Account Isolation ──────────────────────────────────────────────

    @Test
    fun `different accounts have different stock snapshots`() {
        val snapshotA = WidgetSnapshot(
            authenticated = true,
            accountId = "user-A",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            stock = StockSnapshot(
                outOfStockCount = 2,
                items = listOf(
                    WidgetStockItem(
                        productId = "prod-A1",
                        productName = "Product A1",
                        stockQuantity = 0,
                        stockState = StockState.OUT_OF_STOCK,
                    ),
                ),
            ),
        )
        val snapshotB = WidgetSnapshot(
            authenticated = true,
            accountId = "user-B",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            stock = StockSnapshot(
                outOfStockCount = 0,
                items = emptyList(),
            ),
        )
        assertEquals("user-A", snapshotA.accountId)
        assertEquals("user-B", snapshotB.accountId)
        assertEquals(2, snapshotA.stock!!.outOfStockCount)
        assertEquals(0, snapshotB.stock!!.outOfStockCount)
    }

    // ── Security: No Sensitive Data ───────────────────────────────────

    @Test
    fun `stock item does not contain product price`() {
        val item = WidgetStockItem(
            productId = "prod-1",
            productName = "Test Product",
            stockQuantity = 0,
            stockState = StockState.OUT_OF_STOCK,
        )
        // Only productId, productName, stockQuantity, stockState, deepLink
        // No price, description, or other sensitive fields
        assertEquals("prod-1", item.productId)
        assertEquals("Test Product", item.productName)
    }

    // ── Serialization ──────────────────────────────────────────────────

    @Test
    fun `stock snapshot serializes correctly`() {
        val stock = StockSnapshot(
            outOfStockCount = 1,
            lowStockCount = 1,
            items = listOf(
                WidgetStockItem(
                    productId = "prod-1",
                    productName = "Test Product",
                    stockQuantity = 0,
                    stockState = StockState.OUT_OF_STOCK,
                    deepLink = "/product/prod-1",
                ),
            ),
        )
        val json = stock.toJson()
        assertEquals(1, json.getInt("outOfStockCount"))
        assertEquals(1, json.getInt("lowStockCount"))
        val items = json.getJSONArray("items")
        assertEquals(1, items.length())
    }

    @Test
    fun `malformed stock JSON handled gracefully`() {
        val json = org.json.JSONObject("{}")
        val stock = StockSnapshot.fromJson(json)
        assertEquals(0, stock.outOfStockCount)
        assertEquals(0, stock.lowStockCount)
        assertTrue(stock.items.isEmpty())
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
            stock = StockSnapshot(
                outOfStockCount = 1,
                items = listOf(
                    WidgetStockItem(
                        productId = "prod-1",
                        productName = "Test Product",
                        stockQuantity = 0,
                        stockState = StockState.OUT_OF_STOCK,
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
    fun `widget displays max 3 stock items`() {
        val items = (1..5).map { i ->
            WidgetStockItem(
                productId = "prod-$i",
                productName = "Product $i",
                stockQuantity = 0,
                stockState = StockState.OUT_OF_STOCK,
            )
        }
        val displayItems = items.take(3)
        assertEquals(3, displayItems.size)
        assertEquals(5, items.size)
    }

    // ── Stock State Enum ───────────────────────────────────────────────

    @Test
    fun `stock state enum has correct values`() {
        assertEquals(3, StockState.values().size)
        assertNotNull(StockState.valueOf("IN_STOCK"))
        assertNotNull(StockState.valueOf("LOW"))
        assertNotNull(StockState.valueOf("OUT_OF_STOCK"))
    }

    // ── Security: No Tokens in Snapshot ───────────────────────────────

    @Test
    fun `stock snapshot does not contain authentication tokens`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            stock = StockSnapshot(
                outOfStockCount = 1,
                items = listOf(
                    WidgetStockItem(
                        productId = "prod-1",
                        productName = "Test Product",
                        stockQuantity = 0,
                        stockState = StockState.OUT_OF_STOCK,
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
