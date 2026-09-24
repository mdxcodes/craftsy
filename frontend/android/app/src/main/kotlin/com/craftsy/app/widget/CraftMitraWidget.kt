package com.craftsy.app.widget

import android.content.Context
import android.content.Intent
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
 * CraftMitra Quick-Action Widget — one-tap access to Craftsy's AI assistant.
 *
 * This is a lightweight launcher, NOT a second AI implementation.
 * All AI/voice/Bhashini work happens inside the existing CraftMitra Flutter app.
 *
 * Actions:
 * - Speak: Opens CraftMitra (voice-first entry)
 * - Type: Opens CraftMitra (text input)
 *
 * No periodic updates. No AI initialization. No network calls.
 * Only updates on authentication state change.
 */
class CraftMitraWidget : GlanceAppWidget() {

    override suspend fun provideGlance(context: Context, id: GlanceId) {
        val dataStore = WidgetDataStore(context)
        val snapshot = dataStore.loadSnapshot(null)

        provideContent {
            CraftMitraContent(snapshot = snapshot)
        }
    }
}

@Composable
private fun CraftMitraContent(snapshot: WidgetSnapshot?) {
    val backgroundColor = ColorProvider(0xFFFFFFFF.toInt())
    val primaryColor = ColorProvider(0xFF2D3A8C.toInt())
    val textColor = ColorProvider(0xFF1A1A2E.toInt())
    val secondaryTextColor = ColorProvider(0xFF545468.toInt())
    val whiteColor = ColorProvider(0xFFFFFFFF.toInt())

    Box(
        modifier = GlanceModifier
            .fillMaxSize()
            .background(backgroundColor)
            .padding(16.dp),
    ) {
        when {
            snapshot == null || !snapshot.authenticated -> LoggedOutState()
            else -> CraftMitraActionsState(primaryColor, textColor, secondaryTextColor, whiteColor)
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
            text = "CRAFTMITRA",
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
private fun CraftMitraActionsState(
    primaryColor: ColorProvider,
    textColor: ColorProvider,
    secondaryTextColor: ColorProvider,
    whiteColor: ColorProvider,
) {
    Column(
        modifier = GlanceModifier.fillMaxSize(),
    ) {
        // Header
        Text(
            text = "CRAFTMITRA",
            style = TextStyle(
                fontSize = 14.sp,
                fontWeight = FontWeight.Bold,
                color = primaryColor,
            ),
        )

        Spacer(modifier = GlanceModifier.height(4.dp))

        Text(
            text = "How can I help?",
            style = TextStyle(
                fontSize = 12.sp,
                color = secondaryTextColor,
            ),
        )

        Spacer(modifier = GlanceModifier.height(16.dp))

        // Action buttons
        Row(
            modifier = GlanceModifier.fillMaxWidth(),
        ) {
            // Speak button
            Box(
                modifier = GlanceModifier
                    .fillMaxWidth()
                    .height(48.dp)
                    .background(primaryColor)
                    .clickable(actionStartActivity<MainActivity>()),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    text = "Speak",
                    style = TextStyle(
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Bold,
                        color = whiteColor,
                    ),
                )
            }

            Spacer(modifier = GlanceModifier.height(12.dp))

            // Type button
            Box(
                modifier = GlanceModifier
                    .fillMaxWidth()
                    .height(48.dp)
                    .background(ColorProvider(0xFFF5F5FA.toInt()))
                    .clickable(actionStartActivity<MainActivity>()),
                contentAlignment = Alignment.Center,
            ) {
                Text(
                    text = "Type",
                    style = TextStyle(
                        fontSize = 13.sp,
                        fontWeight = FontWeight.Bold,
                        color = textColor,
                    ),
                )
            }
        }

        Spacer(modifier = GlanceModifier.height(12.dp))

        // Description
        Text(
            text = "Voice-first AI assistant for artisans",
            style = TextStyle(
                fontSize = 10.sp,
                color = secondaryTextColor,
            ),
            maxLines = 2,
        )
    }
}
