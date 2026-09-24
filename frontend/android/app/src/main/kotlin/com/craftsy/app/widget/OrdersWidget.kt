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
 * Craftsy Orders Widget — answers "What orders need my attention?"
 *
 * Shows actionable orders (newOrder, packed, shipped) with:
 * - Order ID
 * - Required action (confirm, ship, track)
 * - Product title
 * - Deep link to exact order detail
 *
 * Priority: newOrder > packed > shipped (fulfillment pipeline order)
 */
class OrdersWidget : GlanceAppWidget() {

    override suspend fun provideGlance(context: Context, id: GlanceId) {
        val dataStore = WidgetDataStore(context)
        val snapshot = dataStore.loadSnapshot(null)

        provideContent {
            OrdersContent(snapshot = snapshot)
        }
    }
}

@Composable
private fun OrdersContent(snapshot: WidgetSnapshot?) {
    val backgroundColor = ColorProvider(0xFFFFFFFF.toInt())
    val primaryColor = ColorProvider(0xFF2D3A8C.toInt())
    val textColor = ColorProvider(0xFF1A1A2E.toInt())
    val secondaryTextColor = ColorProvider(0xFF545468.toInt())
    val whiteColor = ColorProvider(0xFFFFFFFF.toInt())
    val warningColor = ColorProvider(0xFFD84343.toInt())
    val infoColor = ColorProvider(0xFFE8912D.toInt())

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
            else -> OrdersListState(snapshot, textColor, secondaryTextColor, primaryColor, whiteColor, warningColor, infoColor)
        }
    }
}

@Composable
private fun LoggedOutState() {
    Column(
        modifier = GlanceModifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(
            text = "CRAFTSY ORDERS",
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
            text = "CRAFTSY ORDERS",
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
private fun OrdersListState(
    snapshot: WidgetSnapshot,
    textColor: ColorProvider,
    secondaryTextColor: ColorProvider,
    primaryColor: ColorProvider,
    whiteColor: ColorProvider,
    warningColor: ColorProvider,
    infoColor: ColorProvider,
) {
    val orders = snapshot.orders
    val actionableCount = orders?.actionableCount ?: 0
    val items = orders?.items ?: emptyList()

    Column(
        modifier = GlanceModifier.fillMaxSize(),
    ) {
        // Header
        Row(
            modifier = GlanceModifier.fillMaxWidth(),
        ) {
            Text(
                text = "ORDERS",
                style = TextStyle(
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    color = primaryColor,
                ),
            )
            Spacer(modifier = GlanceModifier.width(8.dp))
            Text(
                text = "$actionableCount need attention",
                style = TextStyle(
                    fontSize = 12.sp,
                    color = secondaryTextColor,
                ),
            )
        }

        Spacer(modifier = GlanceModifier.height(12.dp))

        if (items.isEmpty()) {
            // Empty state
            Box(
                modifier = GlanceModifier
                    .fillMaxWidth()
                    .height(60.dp),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    text = "No orders need attention",
                    style = TextStyle(
                        fontSize = 12.sp,
                        color = secondaryTextColor,
                    ),
                )
            }
        } else {
            // Order rows (max 3)
            val displayItems = items.take(3)
            for (order in displayItems) {
                OrderRow(
                    order = order,
                    textColor = textColor,
                    secondaryTextColor = secondaryTextColor,
                    primaryColor = primaryColor,
                    warningColor = warningColor,
                    infoColor = infoColor,
                )
                Spacer(modifier = GlanceModifier.height(8.dp))
            }

            // Show count if more orders exist
            if (items.size > 3) {
                Spacer(modifier = GlanceModifier.height(4.dp))
                Text(
                    text = "+${items.size - 3} more",
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
                text = "Open Craftsy",
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
private fun OrderRow(
    order: WidgetOrderSummary,
    textColor: ColorProvider,
    secondaryTextColor: ColorProvider,
    primaryColor: ColorProvider,
    warningColor: ColorProvider,
    infoColor: ColorProvider,
) {
    val actionColor = when (order.status) {
        "newOrder" -> warningColor
        "packed" -> infoColor
        "shipped" -> primaryColor
        else -> secondaryTextColor
    }

    val actionText = order.requiredAction ?: order.statusLabel

    Row(
        modifier = GlanceModifier
            .fillMaxWidth()
            .clickable(actionStartActivity<MainActivity>()),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        // Status indicator dot
        Spacer(
            modifier = GlanceModifier
                .size(8.dp)
                .background(actionColor),
        )

        Spacer(modifier = GlanceModifier.width(8.dp))

        Column(
            modifier = GlanceModifier.defaultWeight(),
        ) {
            // Order ID + action
            Row {
                Text(
                    text = order.orderId,
                    style = TextStyle(
                        fontSize = 12.sp,
                        fontWeight = FontWeight.Bold,
                        color = textColor,
                    ),
                )
                if (actionText.isNotEmpty()) {
                    Spacer(modifier = GlanceModifier.width(6.dp))
                    Text(
                        text = actionText,
                        style = TextStyle(
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Medium,
                            color = actionColor,
                        ),
                    )
                }
            }

            // Product title
            Text(
                text = order.productTitle,
                style = TextStyle(
                    fontSize = 10.sp,
                    color = secondaryTextColor,
                ),
                maxLines = 1,
            )
        }
    }
}
