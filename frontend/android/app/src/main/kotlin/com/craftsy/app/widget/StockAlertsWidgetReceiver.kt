package com.craftsy.app.widget

import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.Log

/**
 * Craftsy Stock Alerts Widget Receiver — handles widget lifecycle events.
 */
class StockAlertsWidgetReceiver : AppWidgetProvider() {

    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray,
    ) {
        Log.d(TAG, "Stock Alerts widget update requested for ${appWidgetIds.size} instances")
    }

    override fun onEnabled(context: Context) {
        Log.d(TAG, "Stock Alerts widget enabled")
    }

    override fun onDisabled(context: Context) {
        Log.d(TAG, "Stock Alerts widget disabled")
    }

    override fun onDeleted(context: Context, appWidgetIds: IntArray) {
        Log.d(TAG, "Stock Alerts widget deleted: ${appWidgetIds.joinToString()}")
    }

    override fun onAppWidgetOptionsChanged(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetId: Int,
        newOptions: Bundle?,
    ) {
        Log.d(TAG, "Stock Alerts widget resized: $appWidgetId")
    }

    companion object {
        private const val TAG = "StockAlertsWidget"
    }
}
