package com.craftsy.app.widget

import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.Log

/**
 * CraftMitra Widget Receiver — handles widget lifecycle events.
 */
class CraftMitraWidgetReceiver : AppWidgetProvider() {

    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray,
    ) {
        Log.d(TAG, "CraftMitra widget update requested for ${appWidgetIds.size} instances")
    }

    override fun onEnabled(context: Context) {
        Log.d(TAG, "CraftMitra widget enabled")
    }

    override fun onDisabled(context: Context) {
        Log.d(TAG, "CraftMitra widget disabled")
    }

    override fun onDeleted(context: Context, appWidgetIds: IntArray) {
        Log.d(TAG, "CraftMitra widget deleted: ${appWidgetIds.joinToString()}")
    }

    override fun onAppWidgetOptionsChanged(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetId: Int,
        newOptions: Bundle?,
    ) {
        Log.d(TAG, "CraftMitra widget resized: $appWidgetId")
    }

    companion object {
        private const val TAG = "CraftMitraWidget"
    }
}
