package com.craftsy.app.widget

import org.json.JSONArray
import org.json.JSONObject

/**
 * Craftsy Widget Snapshot — safe, serializable, versioned.
 *
 * This is the authoritative data model for all Android widgets.
 * It is intentionally decoupled from Flutter/GoRouter/Riverpod internals.
 * Android widgets consume ONLY this model.
 *
 * Schema version is incremented when fields change incompatibly.
 */
data class WidgetSnapshot(
    val schemaVersion: Int = CURRENT_SCHEMA_VERSION,
    val authenticated: Boolean = false,
    val accountId: String? = null,
    val lastUpdated: Long = 0L,
    val dataFreshness: DataFreshness = DataFreshness.UNKNOWN,
    val today: TodaySnapshot? = null,
    val orders: OrdersSnapshot? = null,
    val stock: StockSnapshot? = null,
    val channels: ChannelsSnapshot? = null,
    val craftMitra: CraftMitraSnapshot? = null,
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("schemaVersion", schemaVersion)
        json.put("authenticated", authenticated)
        json.put("accountId", accountId ?: JSONObject.NULL)
        json.put("lastUpdated", lastUpdated)
        json.put("dataFreshness", dataFreshness.name)
        json.put("today", today?.toJson() ?: JSONObject.NULL)
        json.put("orders", orders?.toJson() ?: JSONObject.NULL)
        json.put("stock", stock?.toJson() ?: JSONObject.NULL)
        json.put("channels", channels?.toJson() ?: JSONObject.NULL)
        json.put("craftMitra", craftMitra?.toJson() ?: JSONObject.NULL)
        return json
    }

    companion object {
        const val CURRENT_SCHEMA_VERSION = 1

        fun fromJson(json: JSONObject): WidgetSnapshot {
            return WidgetSnapshot(
                schemaVersion = json.optInt("schemaVersion", 0),
                authenticated = json.optBoolean("authenticated", false),
                accountId = json.optString("accountId").takeIf { it.isNotEmpty() && it != "null" },
                lastUpdated = json.optLong("lastUpdated", 0L),
                dataFreshness = DataFreshness.valueOf(
                    json.optString("dataFreshness", DataFreshness.UNKNOWN.name)
                ),
                today = json.optJSONObject("today")?.let { TodaySnapshot.fromJson(it) },
                orders = json.optJSONObject("orders")?.let { OrdersSnapshot.fromJson(it) },
                stock = json.optJSONObject("stock")?.let { StockSnapshot.fromJson(it) },
                channels = json.optJSONObject("channels")?.let { ChannelsSnapshot.fromJson(it) },
                craftMitra = json.optJSONObject("craftMitra")?.let { CraftMitraSnapshot.fromJson(it) },
            )
        }
    }
}

enum class DataFreshness {
    FRESH,       // Data was just fetched from backend
    STALE,       // Data is from cache but still reasonable
    EXPIRED,     // Data is too old to be trustworthy
    UNKNOWN,      // No timestamp available
}

// ── Today Widget ───────────────────────────────────────────────────────

data class TodaySnapshot(
    val attentionCount: Int = 0,
    val orderAttentionCount: Int = 0,
    val stockAttentionCount: Int = 0,
    val channelAttentionCount: Int = 0,
    val actionableItems: List<ActionableItem> = emptyList(),
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("attentionCount", attentionCount)
        json.put("orderAttentionCount", orderAttentionCount)
        json.put("stockAttentionCount", stockAttentionCount)
        json.put("channelAttentionCount", channelAttentionCount)
        val items = JSONArray()
        for (item in actionableItems) {
            items.put(item.toJson())
        }
        json.put("actionableItems", items)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): TodaySnapshot {
            val items = json.optJSONArray("actionableItems") ?: JSONArray()
            val actionableItems = (0 until items.length()).map { i ->
                ActionableItem.fromJson(items.getJSONObject(i))
            }
            return TodaySnapshot(
                attentionCount = json.optInt("attentionCount", 0),
                orderAttentionCount = json.optInt("orderAttentionCount", 0),
                stockAttentionCount = json.optInt("stockAttentionCount", 0),
                channelAttentionCount = json.optInt("channelAttentionCount", 0),
                actionableItems = actionableItems,
            )
        }
    }
}

data class ActionableItem(
    val type: ActionableType,
    val id: String,
    val title: String,
    val subtitle: String? = null,
    val deepLink: String? = null,
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("type", type.name)
        json.put("id", id)
        json.put("title", title)
        json.put("subtitle", subtitle ?: JSONObject.NULL)
        json.put("deepLink", deepLink ?: JSONObject.NULL)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): ActionableItem {
            return ActionableItem(
                type = ActionableType.valueOf(json.optString("type", ActionableType.ORDER.name)),
                id = json.optString("id", ""),
                title = json.optString("title", ""),
                subtitle = json.optString("subtitle").takeIf { it.isNotEmpty() && it != "null" },
                deepLink = json.optString("deepLink").takeIf { it.isNotEmpty() && it != "null" },
            )
        }
    }
}

enum class ActionableType { ORDER, STOCK, CHANNEL }

// ── Orders Widget ─────────────────────────────────────────────────────

data class OrdersSnapshot(
    val actionableCount: Int = 0,
    val items: List<WidgetOrderSummary> = emptyList(),
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("actionableCount", actionableCount)
        val items = JSONArray()
        for (item in this.items) {
            items.put(item.toJson())
        }
        json.put("items", items)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): OrdersSnapshot {
            val items = json.optJSONArray("items") ?: JSONArray()
            val orderItems = (0 until items.length()).map { i ->
                WidgetOrderSummary.fromJson(items.getJSONObject(i))
            }
            return OrdersSnapshot(
                actionableCount = json.optInt("actionableCount", 0),
                items = orderItems,
            )
        }
    }
}

data class WidgetOrderSummary(
    val orderId: String,
    val status: String,
    val statusLabel: String,
    val productTitle: String,
    val requiredAction: String? = null,
    val deepLink: String? = null,
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("orderId", orderId)
        json.put("status", status)
        json.put("statusLabel", statusLabel)
        json.put("productTitle", productTitle)
        json.put("requiredAction", requiredAction ?: JSONObject.NULL)
        json.put("deepLink", deepLink ?: JSONObject.NULL)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): WidgetOrderSummary {
            return WidgetOrderSummary(
                orderId = json.optString("orderId", ""),
                status = json.optString("status", ""),
                statusLabel = json.optString("statusLabel", ""),
                productTitle = json.optString("productTitle", ""),
                requiredAction = json.optString("requiredAction").takeIf { it.isNotEmpty() && it != "null" },
                deepLink = json.optString("deepLink").takeIf { it.isNotEmpty() && it != "null" },
            )
        }
    }
}

// ── Stock Alerts Widget ───────────────────────────────────────────────

data class StockSnapshot(
    val outOfStockCount: Int = 0,
    val lowStockCount: Int = 0,
    val items: List<WidgetStockItem> = emptyList(),
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("outOfStockCount", outOfStockCount)
        json.put("lowStockCount", lowStockCount)
        val items = JSONArray()
        for (item in this.items) {
            items.put(item.toJson())
        }
        json.put("items", items)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): StockSnapshot {
            val items = json.optJSONArray("items") ?: JSONArray()
            val stockItems = (0 until items.length()).map { i ->
                WidgetStockItem.fromJson(items.getJSONObject(i))
            }
            return StockSnapshot(
                outOfStockCount = json.optInt("outOfStockCount", 0),
                lowStockCount = json.optInt("lowStockCount", 0),
                items = stockItems,
            )
        }
    }
}

data class WidgetStockItem(
    val productId: String,
    val productName: String,
    val stockQuantity: Int,
    val stockState: StockState,
    val deepLink: String? = null,
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("productId", productId)
        json.put("productName", productName)
        json.put("stockQuantity", stockQuantity)
        json.put("stockState", stockState.name)
        json.put("deepLink", deepLink ?: JSONObject.NULL)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): WidgetStockItem {
            return WidgetStockItem(
                productId = json.optString("productId", ""),
                productName = json.optString("productName", ""),
                stockQuantity = json.optInt("stockQuantity", 0),
                stockState = StockState.valueOf(
                    json.optString("stockState", StockState.IN_STOCK.name)
                ),
                deepLink = json.optString("deepLink").takeIf { it.isNotEmpty() && it != "null" },
            )
        }
    }
}

enum class StockState { IN_STOCK, LOW, OUT_OF_STOCK }

// ── Selling Channels Widget ────────────────────────────────────────────

data class ChannelsSnapshot(
    val craftsy: ChannelStatus? = null,
    val ondc: ChannelStatus? = null,
    val government: ChannelStatus? = null,
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("craftsy", craftsy?.toJson() ?: JSONObject.NULL)
        json.put("ondc", ondc?.toJson() ?: JSONObject.NULL)
        json.put("government", government?.toJson() ?: JSONObject.NULL)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): ChannelsSnapshot {
            return ChannelsSnapshot(
                craftsy = json.optJSONObject("craftsy")?.let { ChannelStatus.fromJson(it) },
                ondc = json.optJSONObject("ondc")?.let { ChannelStatus.fromJson(it) },
                government = json.optJSONObject("government")?.let { ChannelStatus.fromJson(it) },
            )
        }
    }
}

data class ChannelStatus(
    val channelName: String,
    val state: ChannelState,
    val stateLabel: String,
    val detail: String? = null,
    val deepLink: String? = null,
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("channelName", channelName)
        json.put("state", state.name)
        json.put("stateLabel", stateLabel)
        json.put("detail", detail ?: JSONObject.NULL)
        json.put("deepLink", deepLink ?: JSONObject.NULL)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): ChannelStatus {
            return ChannelStatus(
                channelName = json.optString("channelName", ""),
                state = ChannelState.valueOf(
                    json.optString("state", ChannelState.NOT_CONFIGURED.name)
                ),
                stateLabel = json.optString("stateLabel", ""),
                detail = json.optString("detail").takeIf { it.isNotEmpty() && it != "null" },
                deepLink = json.optString("deepLink").takeIf { it.isNotEmpty() && it != "null" },
            )
        }
    }
}

/**
 * Widget-friendly channel states. These map from the backend's
 * ONDCChannelStatus/GeMChannelStatus enums to a simpler set
 * that widgets can render without knowing backend internals.
 *
 * NEVER claim CONNECTED/ACTIVE/APPROVED unless the backend state
 * actually supports that claim.
 */
enum class ChannelState {
    ACTIVE,             // Channel is live and operational
    READY,              // Ready to publish/use
    NEEDS_ATTENTION,    // Something requires artisan action
    NOT_CONFIGURED,     // Not set up
    UPDATING,           // Sync/update in progress
    UNAVAILABLE,        // Temporarily unavailable
    ERROR,              // Error state
    PREPARATION_NEEDED, // Assisted workflow - preparation required
}

// ── CraftMitra Widget ─────────────────────────────────────────────────

data class CraftMitraSnapshot(
    val available: Boolean = true,
    val voiceModeAvailable: Boolean = true,
    val textModeAvailable: Boolean = true,
    val voiceDeepLink: String? = "/assistant?mode=voice",
    val textDeepLink: String? = "/assistant?mode=text",
) {
    fun toJson(): JSONObject {
        val json = JSONObject()
        json.put("available", available)
        json.put("voiceModeAvailable", voiceModeAvailable)
        json.put("textModeAvailable", textModeAvailable)
        json.put("voiceDeepLink", voiceDeepLink ?: JSONObject.NULL)
        json.put("textDeepLink", textDeepLink ?: JSONObject.NULL)
        return json
    }

    companion object {
        fun fromJson(json: JSONObject): CraftMitraSnapshot {
            return CraftMitraSnapshot(
                available = json.optBoolean("available", true),
                voiceModeAvailable = json.optBoolean("voiceModeAvailable", true),
                textModeAvailable = json.optBoolean("textModeAvailable", true),
                voiceDeepLink = json.optString("voiceDeepLink").takeIf { it.isNotEmpty() && it != "null" },
                textDeepLink = json.optString("textDeepLink").takeIf { it.isNotEmpty() && it != "null" },
            )
        }
    }
}
