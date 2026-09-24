package com.craftsy.app.widget

import android.appwidget.AppWidgetManager
import android.content.BroadcastReceiver
import android.content.ComponentName
import android.content.Context
import android.content.Intent
import android.util.Log

/**
 * BroadcastReceiver for widget update requests.
 *
 * Receives broadcasts from WidgetUpdateManager and triggers
 * AppWidgetManager to refresh the actual widget UI.
 *
 * This is the bridge between the data layer and the Android
 * widget rendering system.
 */
class WidgetUpdateReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        val action = intent.action ?: return

        when (action) {
            WidgetUpdateManager.ACTION_REFRESH_ALL -> {
                refreshAllWidgets(context)
            }
            WidgetUpdateManager.ACTION_REFRESH_SPECIFIC -> {
                val widgetClassName = intent.getStringExtra(WidgetUpdateManager.EXTRA_WIDGET_CLASS)
                if (widgetClassName != null) {
                    refreshSpecificWidget(context, widgetClassName)
                }
            }
        }
    }

    private fun refreshAllWidgets(context: Context) {
        val appWidgetManager = AppWidgetManager.getInstance(context)

        // Refresh each widget type that exists
        // All 5 widgets now registered
        val widgetClasses = listOf(
            CraftsyTodayWidget::class.java,
            OrdersWidget::class.java,
            StockAlertsWidget::class.java,
            CraftMitraWidget::class.java,
            SellingChannelsWidget::class.java,
        )

        for (widgetClass in widgetClasses) {
            val componentName = ComponentName(context, widgetClass)
            val appWidgetIds = appWidgetManager.getAppWidgetIds(componentName)
            if (appWidgetIds.isNotEmpty()) {
                // For Glance widgets, trigger update via AppWidgetManager
                // The GlanceAppWidget's provideGlance will read the latest snapshot
                val updateIntent = Intent(context, widgetClass).apply {
                    action = AppWidgetManager.ACTION_APPWIDGET_UPDATE
                    putExtra(AppWidgetManager.EXTRA_APPWIDGET_IDS, appWidgetIds)
                }
                context.sendBroadcast(updateIntent)
                Log.d(TAG, "Triggered update for ${widgetClass.simpleName}: ${appWidgetIds.size} instances")
            }
        }
    }

    private fun refreshSpecificWidget(context: Context, widgetClassName: String) {
        try {
            val widgetClass = Class.forName(widgetClassName)
            val componentName = ComponentName(context, widgetClass)
            val appWidgetManager = AppWidgetManager.getInstance(context)
            val appWidgetIds = appWidgetManager.getAppWidgetIds(componentName)
            if (appWidgetIds.isNotEmpty()) {
                val updateIntent = Intent(context, widgetClass).apply {
                    action = AppWidgetManager.ACTION_APPWIDGET_UPDATE
                    putExtra(AppWidgetManager.EXTRA_APPWIDGET_IDS, appWidgetIds)
                }
                context.sendBroadcast(updateIntent)
            }
        } catch (e: ClassNotFoundException) {
            Log.w(TAG, "Widget class not found: $widgetClassName")
        }
    }

    companion object {
        private const val TAG = "WidgetUpdateReceiver"
    }
}
