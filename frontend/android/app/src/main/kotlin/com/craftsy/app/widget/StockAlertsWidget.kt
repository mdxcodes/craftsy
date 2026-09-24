package com.craftsy.app.widget

import android.content.Context
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.glance.GlanceId
import androidx.glance.GlanceModifier
import androidx.glance.action.actionStartActivity
import androidx.glance.action.clickable
import androidx.glance.appwidget.GlanceAppWidget
import androidx.glance.appwidget.provideContent
import androidx.glance.background
import androidx.glance.layout.Alignment
import androidx.glance.layout.Box
import androidx.glance.layout.Column
import androidx.glance.layout.Row
import androidx.glance.layout.Spacer
import androidx.glance.layout.fillMaxSize
import androidx.glance.layout.fillMaxWidth
import androidx.glance.layout.height
import androidx.glance.layout.padding
import androidx.glance.layout.size
import androidx.glance.layout.width
import androidx.glance.text.FontWeight
import androidx.glance.text.Text
import androidx.glance.text.TextStyle
import androidx.glance.unit.ColorProvider
import com.craftsy.app.MainActivity

/**
 * Craftsy Stock Alerts Widget — answers "Which products need my attention because of stock?"
 *
 * Shows out-of-stock and low-stock products from the local snapshot.
 *
 * Priority: OUT_OF_STOCK > LOW > IN_STOCK
 * Only actionable items (OUT_OF_STOCK, LOW) are displayed.
 * No low-stock threshold is defined by Craftsy — only OUT_OF_STOCK is shown.
 */
class StockAlertsWidget : GlanceAppWidget() {

    override suspend fun provideGlance(context: Context, id: GlanceId) {
        val dataStore = WidgetDataStore(context)
        val snapshot = dataStore.loadSnapshot(null)

        provideContent {
            StockAlertsContent(snapshot = snapshot)
        }
    }
}

@Composable
private fun StockAlertsContent(snapshot: WidgetSnapshot?) {
    val backgroundColor = ColorProvider(0xFFFFFFFF.toInt())
    val primaryColor = ColorProvider(0xFF2D3A8C.toInt())
    val textColor = ColorProvider(0xFF1A1A2E.toInt())
    val secondaryTextColor = ColorProvider(0xFF545468.toInt())
    val whiteColor = ColorProvider(0xFFFFFFFF.toInt())
    val errorColor = ColorProvider(0xFFD84343.toInt())
    val warningColor = ColorProvider(0xFFE8912D.toInt())

    Box(
        modifier = GlanceModifier
            .fillMaxSize()
            .background(backgroundColor)
            .padding(16.dp),
    ) {
        when {
            snapshot == null || !snapshot.authenticated -> LoggedOutState()
            snapshot.dataFreshness == DataFreshness.UNKNOWN ||
                snapshot.dataFreshness == DataFreshness.EXPIRED -> DataUnavailableState()
            else -> StockAlertsListState(
                snapshot,
                textColor,
                secondaryTextColor,
                primaryColor,
                whiteColor,
                errorColor,
                warningColor,
            )
        }
    }
}

@Composable
private fun LoggedOutState() {
    Column(
        modifier = GlanceModifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Text(
            text = "CRAFTSY STOCK",
            style = TextStyle(
                fontSize = 14.sp,
                fontWeight = FontWeight.Bold,
                color = ColorProvider(0xFF2D3A8C.toInt()),
            ),
        )
        Spacer(modifier = GlanceModifier.height(8.dp))
        Text(
            text = "Open Craftsy to sign in",
            style = TextStyle(
                fontSize = 12.sp,
                color = ColorProvider(0xFF545468.toInt()),
            ),
        )
    }
}

@Composable
private fun DataUnavailableState() {
    Column(
        modifier = GlanceModifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(
            text = "CRAFTSY STOCK",
            style = TextStyle(
                fontSize = 14.sp,
                fontWeight = FontWeight.Bold,
                color = ColorProvider(0xFF2D3A8C.toInt()),
            ),
        )
        Spacer(modifier = GlanceModifier.height(8.dp))
        Text(
            text = "Open Craftsy to update",
            style = TextStyle(
                fontSize = 12.sp,
                color = ColorProvider(0xFF545468.toInt()),
            ),
        )
    }
}

@Composable
private fun StockAlertsListState(
    snapshot: WidgetSnapshot,
    textColor: ColorProvider,
    secondaryTextColor: ColorProvider,
    primaryColor: ColorProvider,
    whiteColor: ColorProvider,
    errorColor: ColorProvider,
    warningColor: ColorProvider,
) {
    val stock = snapshot.stock
    val outOfStockCount = stock?.outOfStockCount ?: 0
    val lowStockCount = stock?.lowStockCount ?: 0
    val items = stock?.items ?: emptyList()
    val totalAlerts = outOfStockCount + lowStockCount

    Column(
        modifier = GlanceModifier.fillMaxSize(),
    ) {
        // Header
        Row(
            modifier = GlanceModifier.fillMaxWidth(),
        ) {
            Text(
                text = "STOCK ALERTS",
                style = TextStyle(
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    color = primaryColor,
                ),
            )
            if (totalAlerts > 0) {
                Spacer(modifier = GlanceModifier.width(8.dp))
                Text(
                    text = "$totalAlerts need attention",
                    style = TextStyle(
                        fontSize = 12.sp,
                        color = secondaryTextColor,
                    ),
                )
            }
        }

        Spacer(modifier = GlanceModifier.height(12.dp))

        if (totalAlerts == 0) {
            // Empty state
            Box(
                modifier = GlanceModifier
                    .fillMaxWidth()
                    .height(60.dp),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    text = "Stock looks good",
                    style = TextStyle(
                        fontSize = 12.sp,
                        color = secondaryTextColor,
                    ),
                )
            }
        } else {
            // Show out-of-stock items first
            val actionableItems = items
                .filter { it.stockState == StockState.OUT_OF_STOCK || it.stockState == StockState.LOW }
                .sortedBy {
                    when (it.stockState) {
                        StockState.OUT_OF_STOCK -> 0
                        StockState.LOW -> 1
                        else -> 2
                    }
                }
                .take(3)

            for (item in actionableItems) {
                StockItemRow(
                    item = item,
                    textColor = textColor,
                    secondaryTextColor = secondaryTextColor,
                    errorColor = errorColor,
                    warningColor = warningColor,
                )
                Spacer(modifier = GlanceModifier.height(8.dp))
            }

            // Show count if more items exist
            if (actionableItems.size < items.count {
                it.stockState == StockState.OUT_OF_STOCK || it.stockState == StockState.LOW
            }) {
                Spacer(modifier = GlanceModifier.height(4.dp))
                Text(
                    text = "+${items.count { it.stockState == StockState.OUT_OF_STOCK || it.stockState == StockState.LOW } - actionableItems.size} more",
                    style = TextStyle(
                        fontSize = 10.sp,
                        color = secondaryTextColor,
                    ),
                )
            }
        }

        Spacer(modifier = GlanceModifier.height(8.dp))

        // Open Craftsy button
        Box(
            modifier = GlanceModifier
                .fillMaxWidth()
                .height(36.dp)
                .background(primaryColor)
                .clickable(actionStartActivity<MainActivity>()),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = "View Inventory",
                style = TextStyle(
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    color = whiteColor,
                ),
            )
        }
    }
}

@Composable
private fun StockItemRow(
    item: WidgetStockItem,
    textColor: ColorProvider,
    secondaryTextColor: ColorProvider,
    errorColor: ColorProvider,
    warningColor: ColorProvider,
) {
    val stateColor = when (item.stockState) {
        StockState.OUT_OF_STOCK -> errorColor
        StockState.LOW -> warningColor
        StockState.IN_STOCK -> secondaryTextColor
    }

    val stateLabel = when (item.stockState) {
        StockState.OUT_OF_STOCK -> "Out of stock"
        StockState.LOW -> if (item.stockQuantity > 0) "${item.stockQuantity} left" else "Low stock"
        StockState.IN_STOCK -> "In stock"
    }

    Row(
        modifier = GlanceModifier
            .fillMaxWidth()
            .clickable(actionStartActivity<MainActivity>()),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        // State indicator dot
        Spacer(
            modifier = GlanceModifier
                .size(8.dp)
                .background(stateColor),
        )

        Spacer(modifier = GlanceModifier.width(8.dp))

        Column(
            modifier = GlanceModifier.defaultWeight(),
        ) {
            Text(
                text = item.productName,
                style = TextStyle(
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Medium,
                    color = textColor,
                ),
                maxLines = 1,
            )
            Text(
                text = stateLabel,
                style = TextStyle(
                    fontSize = 10.sp,
                    color = stateColor,
                ),
                maxLines = 1,
            )
        }
    }
}
