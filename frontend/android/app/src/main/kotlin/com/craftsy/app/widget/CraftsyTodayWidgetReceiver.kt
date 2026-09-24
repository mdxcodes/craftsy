package com.craftsy.app.widget

import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.Log

/**
 * Craftsy Today Widget Receiver — handles widget lifecycle events.
 *
 * This is the entry point for the Android widget system.
 * It delegates to the GlanceAppWidget (CraftsyTodayWidget) for rendering
 * and handles lifecycle events like updates, enable/disable, and deletion.
 *
 * For Glance widgets, we use AppWidgetManager to trigger updates.
 * The GlanceAppWidget's provideGlance will be called by the system
 * when the widget needs to be rendered or updated.
 */
class CraftsyTodayWidgetReceiver : AppWidgetProvider() {

    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray,
    ) {
        // For Glance widgets, the system calls provideGlance automatically
        // when the widget needs to be rendered. We just need to ensure
        // the widget is properly configured.
        Log.d(TAG, "Craftsy Today widget update requested for ${appWidgetIds.size} instances")
    }

    override fun onEnabled(context: Context) {
        // First widget instance added — initialize if needed
        Log.d(TAG, "Craftsy Today widget enabled")
    }

    override fun onDisabled(context: Context) {
        // Last widget instance removed — clean up if needed
        Log.d(TAG, "Craftsy Today widget disabled")
    }

    override fun onDeleted(context: Context, appWidgetIds: IntArray) {
        // Widget instance deleted — clean up any instance-specific data
        Log.d(TAG, "Craftsy Today widget deleted: ${appWidgetIds.joinToString()}")
    }

    override fun onAppWidgetOptionsChanged(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetId: Int,
        newOptions: Bundle?,
    ) {
        // Widget resized — Glance handles responsive layouts automatically
        // via the SizeMode.Responsive we defined in CraftsyTodayWidget
        Log.d(TAG, "Craftsy Today widget resized: $appWidgetId")
    }

    companion object {
        private const val TAG = "CraftsyTodayWidget"
    }
}
