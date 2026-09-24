package com.craftsy.app.widget

import android.content.Context
import android.content.SharedPreferences
import org.json.JSONObject

/**
 * Persistent storage for widget snapshots.
 *
 * Uses SharedPreferences — lightweight, sufficient for small snapshots,
 * no need for a full database. Stores the JSON representation of
 * [WidgetSnapshot] keyed by schema version.
 *
 * Account isolation: each snapshot is stored under the account ID.
 * When account changes, old snapshots are cleared.
 */
class WidgetDataStore(context: Context) {

    private val prefs: SharedPreferences =
        context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    /**
     * Save snapshot for the given account.
     * If accountId is null, stores under a default key (for pre-auth state).
     */
    fun saveSnapshot(snapshot: WidgetSnapshot, accountId: String?) {
        val key = snapshotKey(accountId)
        prefs.edit()
            .putString(key, snapshot.toJson().toString())
            .putLong("${key}_timestamp", System.currentTimeMillis())
            .apply()
    }

    /**
     * Load snapshot for the given account.
     * Returns null if no snapshot exists or data is corrupted.
     */
    fun loadSnapshot(accountId: String?): WidgetSnapshot? {
        val key = snapshotKey(accountId)
        val jsonStr = prefs.getString(key, null) ?: return null
        return try {
            val json = JSONObject(jsonStr)
            // Version check — discard incompatible snapshots
            val version = json.optInt("schemaVersion", 0)
            if (version != WidgetSnapshot.CURRENT_SCHEMA_VERSION) {
                null
            } else {
                WidgetSnapshot.fromJson(json)
            }
        } catch (e: Exception) {
            // Corrupt data — safely discard
            null
        }
    }

    /**
     * Clear all widget data for the given account.
     * Called on logout or account switch.
     */
    fun clearAccount(accountId: String?) {
        val key = snapshotKey(accountId)
        prefs.edit()
            .remove(key)
            .remove("${key}_timestamp")
            .apply()
    }

    /**
     * Clear ALL widget data. Used on full logout or data clear.
     */
    fun clearAll() {
        prefs.edit().clear().apply()
    }

    /**
     * Get the timestamp of the last snapshot for staleness checks.
     */
    fun getLastUpdateTime(accountId: String?): Long {
        val key = snapshotKey(accountId)
        return prefs.getLong("${key}_timestamp", 0L)
    }

    /**
     * Check if snapshot exists and is not stale.
     */
    fun hasValidSnapshot(accountId: String?, maxStaleMs: Long): Boolean {
        val snapshot = loadSnapshot(accountId) ?: return false
        val timestamp = getLastUpdateTime(accountId)
        val age = System.currentTimeMillis() - timestamp
        return age <= maxStaleMs
    }

    private fun snapshotKey(accountId: String?): String {
        return if (accountId != null) {
            "widget_snapshot_$accountId"
        } else {
            "widget_snapshot_default"
        }
    }

    companion object {
        private const val PREFS_NAME = "craftsy_widget_data"

        /** Default staleness threshold: 2 hours */
        const val DEFAULT_MAX_STALE_MS = 2 * 60 * 60 * 1000L
    }
}
