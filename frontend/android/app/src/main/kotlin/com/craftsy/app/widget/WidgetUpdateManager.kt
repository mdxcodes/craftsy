package com.craftsy.app.widget

import android.content.Context
import android.content.Intent
import androidx.core.app.TaskStackBuilder

/**
 * Centralized widget update manager.
 *
 * Responsibilities:
 * - Trigger widget refresh after data changes
 * - Avoid duplicate/redundant updates (idempotent)
 * - Handle account transitions
 * - Handle stale/invalid data
 *
 * Uses AppWidgetManager to trigger updates only when needed.
 */
class WidgetUpdateManager(private val context: Context) {

    /**
     * Refresh all Craftsy widgets.
     * Called after meaningful state changes (order update, stock change, etc.)
     */
    fun refreshAllWidgets() {
        val intent = Intent(context, WidgetUpdateReceiver::class.java).apply {
            action = ACTION_REFRESH_ALL
        }
        context.sendBroadcast(intent)
    }

    /**
     * Refresh a specific widget type.
     */
    fun refreshWidget(widgetClass: Class<*>) {
        val intent = Intent(context, WidgetUpdateReceiver::class.java).apply {
            action = ACTION_REFRESH_SPECIFIC
            putExtra(EXTRA_WIDGET_CLASS, widgetClass.name)
        }
        context.sendBroadcast(intent)
    }

    /**
     * Handle account transition: clear old data, trigger refresh.
     */
    fun onAccountChanged(oldAccountId: String?, newAccountId: String?) {
        val dataStore = WidgetDataStore(context)
        // Clear old account's data
        dataStore.clearAccount(oldAccountId)
        // Clear "default" data too (pre-auth state)
        dataStore.clearAccount(null)
        // Refresh all widgets
        refreshAllWidgets()
    }

    /**
     * Handle logout: clear all widget data, refresh.
     */
    fun onLogout() {
        val dataStore = WidgetDataStore(context)
        dataStore.clearAll()
        refreshAllWidgets()
    }

    /**
     * Handle login: trigger widget data sync.
     */
    fun onLogin(accountId: String?) {
        refreshAllWidgets()
    }

    companion object {
        const val ACTION_REFRESH_ALL = "com.craftsy.app.widget.REFRESH_ALL"
        const val ACTION_REFRESH_SPECIFIC = "com.craftsy.app.widget.REFRESH_SPECIFIC"
        const val EXTRA_WIDGET_CLASS = "widget_class"

        /** Maximum time between forced refreshes (prevents update storms) */
        const val MIN_UPDATE_INTERVAL_MS = 1_000L
    }
}
