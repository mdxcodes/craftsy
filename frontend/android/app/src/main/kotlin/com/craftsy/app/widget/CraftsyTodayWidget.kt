package com.craftsy.app.widget

import android.content.Context
import androidx.compose.runtime.Composable
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.glance.GlanceId
import androidx.glance.GlanceModifier
import androidx.glance.GlanceTheme
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
 * Craftsy Today Widget — answers "What needs my attention today?"
 *
 * Reads the real widget snapshot from WidgetDataStore and renders
 * actionable items: orders, stock alerts, channel attention.
 */
class CraftsyTodayWidget : GlanceAppWidget() {

    override suspend fun provideGlance(context: Context, id: GlanceId) {
        val dataStore = WidgetDataStore(context)
        val snapshot = dataStore.loadSnapshot(null)

        provideContent {
            GlanceTheme {
                CraftsyTodayContent(snapshot = snapshot)
            }
        }
    }
}

@Composable
private fun CraftsyTodayContent(snapshot: WidgetSnapshot?) {
    val primaryColor = ColorProvider(0xFF2D3A8C.toInt())
    val textColor = ColorProvider(0xFF1A1A2E.toInt())
    val secondaryTextColor = ColorProvider(0xFF545468.toInt())
    val whiteColor = ColorProvider(0xFFFFFFFF.toInt())

    Box(
        modifier = GlanceModifier
            .fillMaxSize()
            .background(GlanceTheme.colors.background)
            .padding(16.dp),
    ) {
        when {
            snapshot == null || !snapshot.authenticated -> LoggedOutState()
            snapshot.dataFreshness == DataFreshness.UNKNOWN ||
                snapshot.dataFreshness == DataFreshness.EXPIRED -> DataUnavailableState()
            snapshot.dataFreshness == DataFreshness.STALE -> {
                StaleDataBanner()
                AttentionContent(snapshot, textColor, secondaryTextColor, primaryColor, whiteColor)
            }
            else -> AttentionContent(snapshot, textColor, secondaryTextColor, primaryColor, whiteColor)
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
            text = "CRAFTSY",
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
            text = "CRAFTSY",
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
private fun StaleDataBanner() {
    Row(
        modifier = GlanceModifier
            .fillMaxWidth()
            .background(ColorProvider(0xFFFFF3E0.toInt()))
            .padding(horizontal = 8.dp, vertical = 4.dp),
    ) {
        Text(
            text = "Updated recently",
            style = TextStyle(
                fontSize = 10.sp,
                color = ColorProvider(0xFFC75B39.toInt()),
            ),
        )
    }
}

@Composable
private fun AttentionContent(
    snapshot: WidgetSnapshot,
    textColor: ColorProvider,
    secondaryTextColor: ColorProvider,
    primaryColor: ColorProvider,
    whiteColor: ColorProvider,
) {
    val today = snapshot.today ?: return

    Column(
        modifier = GlanceModifier.fillMaxSize(),
    ) {
        Row(
            modifier = GlanceModifier.fillMaxWidth(),
        ) {
            Text(
                text = "CRAFTSY",
                style = TextStyle(
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    color = primaryColor,
                ),
            )
            Spacer(modifier = GlanceModifier.width(8.dp))
            Text(
                text = "${today.attentionCount} need attention",
                style = TextStyle(
                    fontSize = 12.sp,
                    color = secondaryTextColor,
                ),
            )
        }

        Spacer(modifier = GlanceModifier.height(12.dp))

        val items = today.actionableItems.take(3)
        for (item in items) {
            ActionableItemRow(
                item = item,
                textColor = textColor,
                secondaryTextColor = secondaryTextColor,
            )
            Spacer(modifier = GlanceModifier.height(8.dp))
        }

        Spacer(modifier = GlanceModifier.height(4.dp))
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
private fun ActionableItemRow(
    item: ActionableItem,
    textColor: ColorProvider,
    secondaryTextColor: ColorProvider,
) {
    val typeColor = when (item.type) {
        ActionableType.ORDER -> ColorProvider(0xFF2D3A8C.toInt())
        ActionableType.STOCK -> ColorProvider(0xFFD84343.toInt())
        ActionableType.CHANNEL -> ColorProvider(0xFFE8912D.toInt())
    }

    Row(
        modifier = GlanceModifier
            .fillMaxWidth()
            .clickable(actionStartActivity<MainActivity>()),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Spacer(
            modifier = GlanceModifier
                .size(8.dp)
                .background(typeColor),
        )

        Spacer(modifier = GlanceModifier.width(8.dp))

        Column(
            modifier = GlanceModifier.defaultWeight(),
        ) {
            Text(
                text = item.title,
                style = TextStyle(
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Medium,
                    color = textColor,
                ),
                maxLines = 1,
            )
            if (item.subtitle != null) {
                Text(
                    text = item.subtitle!!,
                    style = TextStyle(
                        fontSize = 10.sp,
                        color = secondaryTextColor,
                    ),
                    maxLines = 1,
                )
            }
        }
    }
}
