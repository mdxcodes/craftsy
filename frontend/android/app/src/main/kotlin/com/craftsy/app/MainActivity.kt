package com.craftsy.app

import android.content.ActivityNotFoundException
import android.content.Intent
import android.speech.tts.TextToSpeech
import androidx.core.content.FileProvider
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import org.json.JSONObject
import java.io.File

class MainActivity : FlutterActivity() {
    private val CHANNEL = "com.craftsy.app/whatsapp_share"
    private val ttsVoiceDataChannel = "craftsy/tts_voice_data"
    private val widgetDataChannel = "com.craftsy.app/widget_data"

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        // 1. WhatsApp Share Channel (From your PR)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler { call, result ->
            if (call.method == "shareToWhatsApp") {
                val imagePath = call.argument<String>("imagePath")
                val text = call.argument<String>("text") ?: ""

                try {
                    val intent = Intent(Intent.ACTION_SEND).apply {
                        type = "image/*"
                        putExtra(Intent.EXTRA_TEXT, text)
                        setPackage("com.whatsapp")
                        if (!imagePath.isNullOrEmpty()) {
                            val file = File(imagePath)
                            if (file.exists()) {
                                val contentUri = FileProvider.getUriForFile(
                                    context,
                                    "${context.packageName}.fileprovider",
                                    file
                                )
                                putExtra(Intent.EXTRA_STREAM, contentUri)
                                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                            }
                        }
                    }
                    startActivity(intent)
                    result.success(true)
                } catch (e: ActivityNotFoundException) {
                    result.success(false)
                } catch (e: Exception) {
                    result.error("SHARE_ERROR", e.localizedMessage, null)
                }
            } else {
                result.notImplemented()
            }
        }

        // 2. TTS Voice Data Installer Channel (From main)
        // Bridges AppTtsService.openVoiceDownloadScreen() to Android's native
        // voice-data download screen. Flutter cannot reach this on its own —
        // without it, a missing voice pack means the user has to find
        // Settings > System > Languages > Text-to-speech > Install voice data
        // themselves, in whatever language the OS happens to be in.
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, ttsVoiceDataChannel)
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "openVoiceDataInstaller" -> openVoiceDataInstaller(result)
                    else -> result.notImplemented()
                }
            }

        // 3. Widget Data Channel — receives snapshots from Flutter
        // This is the bridge between Flutter's widget snapshot provider
        // and Android's native widget rendering layer.
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, widgetDataChannel)
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "updateWidgetData" -> {
                        val json = call.argument<Map<String, Any?>>("data")
                        if (json != null) {
                            try {
                                val snapshot = JSONObject(json)
                                val dataStore = com.craftsy.app.widget.WidgetDataStore(applicationContext)
                                val accountId = snapshot.optString("accountId")
                                    .takeIf { it.isNotEmpty() && it != "null" }
                                val widgetSnapshot =
                                    com.craftsy.app.widget.WidgetSnapshot.fromJson(snapshot)
                                dataStore.saveSnapshot(widgetSnapshot, accountId)
                                result.success(true)
                            } catch (e: Exception) {
                                result.error("PARSE_ERROR", e.localizedMessage, null)
                            }
                        } else {
                            result.error("NO_DATA", "No widget data provided", null)
                        }
                    }
                    "clearWidgetData" -> {
                        val dataStore = com.craftsy.app.widget.WidgetDataStore(applicationContext)
                        dataStore.clearAll()
                        result.success(true)
                    }
                    "refreshWidgets" -> {
                        val updateManager =
                            com.craftsy.app.widget.WidgetUpdateManager(applicationContext)
                        updateManager.refreshAllWidgets()
                        result.success(true)
                    }
                    else -> result.notImplemented()
                }
            }
    }

    private fun openVoiceDataInstaller(result: MethodChannel.Result) {
        try {
            val intent = Intent().apply {
                action = TextToSpeech.Engine.ACTION_INSTALL_TTS_DATA
                flags = Intent.FLAG_ACTIVITY_NEW_TASK
            }

            if (intent.resolveActivity(packageManager) == null) {
                result.success(false)
                return
            }

            startActivity(intent)
            result.success(true)
        } catch (e: Exception) {
            result.success(false)
        }
    }
}
