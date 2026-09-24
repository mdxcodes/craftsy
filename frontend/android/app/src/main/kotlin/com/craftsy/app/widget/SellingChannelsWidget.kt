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
 * Craftsy Selling Channels Widget — answers "Where am I selling, and what do I need to do?"
 *
 * Shows the actual state of each selling channel:
 * - Craftsy: Active (native marketplace)
 * - ONDC: Actual state (NOT_CONFIGURED until real API onboarding)
 * - Government/GeM: Actual state (NOT_CONFIGURED until real API onboarding)
 *
 * TRUTHFULNESS: This widget NEVER claims a channel is connected/active
 * unless the existing Craftsy implementation actually proves that state.
 * ONDC and GeM currently show NOT_CONFIGURED — they are scaffolds only.
 *
 * No periodic updates. No network calls. Renders from local snapshot only.
 */
class SellingChannelsWidget : GlanceAppWidget() {

    override suspend fun provideGlance(context: Context, id: GlanceId) {
        val dataStore = WidgetDataStore(context)
        val snapshot = dataStore.loadSnapshot(null)

        provideContent {
            SellingChannelsContent(snapshot = snapshot)
        }
    }
}

@Composable
private fun SellingChannelsContent(snapshot: WidgetSnapshot?) {
    val backgroundColor = ColorProvider(0xFFFFFFFF.toInt())
    val primaryColor = ColorProvider(0xFF2D3A8C.toInt())
    val textColor = ColorProvider(0xFF1A1A2E.toInt())
    val secondaryTextColor = ColorProvider(0xFF545468.toInt())
    val whiteColor = ColorProvider(0xFFFFFFFF.toInt())
    val successColor = ColorProvider(0xFF00696E.toInt())
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
            else -> ChannelsListState(
                snapshot,
                textColor,
                secondaryTextColor,
                primaryColor,
                whiteColor,
                successColor,
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
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(
            text = "SELLING CHANNELS",
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
            text = "SELLING CHANNELS",
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
private fun ChannelsListState(
    snapshot: WidgetSnapshot,
    textColor: ColorProvider,
    secondaryTextColor: ColorProvider,
    primaryColor: ColorProvider,
    whiteColor: ColorProvider,
    successColor: ColorProvider,
    warningColor: ColorProvider,
) {
    val channels = snapshot.channels

    Column(
        modifier = GlanceModifier.fillMaxSize(),
    ) {
        // Header
        Row(
            modifier = GlanceModifier.fillMaxWidth(),
        ) {
            Text(
                text = "SELLING CHANNELS",
                style = TextStyle(
                    fontSize = 14.sp,
                    fontWeight = FontWeight.Bold,
                    color = primaryColor,
                ),
            )
        }

        Spacer(modifier = GlanceModifier.height(12.dp))

        // Craftsy channel
        channels?.craftsy?.let { channel ->
            ChannelRow(
                channel = channel,
                textColor = textColor,
                secondaryTextColor = secondaryTextColor,
                successColor = successColor,
                warningColor = warningColor,
            )
            Spacer(modifier = GlanceModifier.height(8.dp))
        }

        // ONDC channel
        channels?.ondc?.let { channel ->
            ChannelRow(
                channel = channel,
                textColor = textColor,
                secondaryTextColor = secondaryTextColor,
                successColor = successColor,
                warningColor = warningColor,
            )
            Spacer(modifier = GlanceModifier.height(8.dp))
        }

        // Government channel
        channels?.government?.let { channel ->
            ChannelRow(
                channel = channel,
                textColor = textColor,
                secondaryTextColor = secondaryTextColor,
                successColor = successColor,
                warningColor = warningColor,
            )
            Spacer(modifier = GlanceModifier.height(8.dp))
        }

        Spacer(modifier = GlanceModifier.height(4.dp))

        // Sell & Grow button
        Box(
            modifier = GlanceModifier
                .fillMaxWidth()
                .height(36.dp)
                .background(primaryColor)
                .clickable(actionStartActivity<MainActivity>()),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = "Sell & Grow",
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
private fun ChannelRow(
    channel: ChannelStatus,
    textColor: ColorProvider,
    secondaryTextColor: ColorProvider,
    successColor: ColorProvider,
    warningColor: ColorProvider,
) {
    val stateColor = when (channel.state) {
        ChannelState.ACTIVE -> successColor
        ChannelState.READY -> successColor
        ChannelState.NEEDS_ATTENTION -> warningColor
        ChannelState.NOT_CONFIGURED -> secondaryTextColor
        ChannelState.UPDATING -> warningColor
        ChannelState.UNAVAILABLE -> warningColor
        ChannelState.ERROR -> warningColor
        ChannelState.PREPARATION_NEEDED -> warningColor
    }

    val stateLabel = channel.stateLabel.ifEmpty { channel.state.name }

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
                text = channel.channelName,
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
            if (channel.detail != null && channel.detail.isNotEmpty()) {
                Text(
                    text = channel.detail,
                    style = TextStyle(
                        fontSize = 9.sp,
                        color = secondaryTextColor,
                    ),
                    maxLines = 1,
                )
            }
        }
    }
}
