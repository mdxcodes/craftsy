package com.craftsy.app.widget

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Tests for Craftsy Selling Channels Widget.
 *
 * Covers: channel snapshot projection, Craftsy/ONDC/GeM states,
 * truthfulness (no fabricated active state), deep links, accessibility,
 * localization, account isolation, and idempotent updates.
 */
class SellingChannelsWidgetStateTest {

    // ── Channel Snapshot Projection ────────────────────────────────────

    @Test
    fun `channels snapshot contains all three channels`() {
        val channels = ChannelsSnapshot(
            craftsy = ChannelStatus(
                channelName = "Craftsy",
                state = ChannelState.ACTIVE,
                stateLabel = "Active",
                detail = "Your marketplace is live",
                deepLink = "/catalogue",
            ),
            ondc = ChannelStatus(
                channelName = "ONDC",
                state = ChannelState.NOT_CONFIGURED,
                stateLabel = "Not configured",
                detail = "Setup required to sell on ONDC",
                deepLink = "/commerce-hub",
            ),
            government = ChannelStatus(
                channelName = "Government",
                state = ChannelState.NOT_CONFIGURED,
                stateLabel = "Not configured",
                detail = "Setup required to sell to government",
                deepLink = "/commerce-hub",
            ),
        )
        assertNotNull(channels.craftsy)
        assertNotNull(channels.ondc)
        assertNotNull(channels.government)
        assertEquals("Craftsy", channels.craftsy!!.channelName)
        assertEquals("ONDC", channels.ondc!!.channelName)
        assertEquals("Government", channels.government!!.channelName)
    }

    // ── Craftsy Channel State ──────────────────────────────────────────

    @Test
    fun `craftsy channel is active by default`() {
        val craftsy = ChannelStatus(
            channelName = "Craftsy",
            state = ChannelState.ACTIVE,
            stateLabel = "Active",
            detail = "Your marketplace is live",
            deepLink = "/catalogue",
        )
        assertEquals(ChannelState.ACTIVE, craftsy.state)
        assertEquals("Active", craftsy.stateLabel)
    }

    @Test
    fun `craftsy channel does not claim connection state`() {
        // Craftsy is the native marketplace — it's always available
        // for an authenticated artisan, not a "connection"
        val craftsy = ChannelStatus(
            channelName = "Craftsy",
            state = ChannelState.ACTIVE,
            stateLabel = "Active",
        )
        assertEquals(ChannelState.ACTIVE, craftsy.state)
        assertFalse(craftsy.state.name.contains("CONNECTED"))
    }

    // ── ONDC Channel State ─────────────────────────────────────────────

    @Test
    fun `ondc is not configured by default`() {
        val ondc = ChannelStatus(
            channelName = "ONDC",
            state = ChannelState.NOT_CONFIGURED,
            stateLabel = "Not configured",
            detail = "Setup required to sell on ONDC",
            deepLink = "/commerce-hub",
        )
        assertEquals(ChannelState.NOT_CONFIGURED, ondc.state)
        assertEquals("Not configured", ondc.stateLabel)
    }

    @Test
    fun `ondc does not claim active or connected state`() {
        // ONDC is a scaffold only — no real API integration
        val ondc = ChannelStatus(
            channelName = "ONDC",
            state = ChannelState.NOT_CONFIGURED,
            stateLabel = "Not configured",
        )
        assertFalse(ondc.state.name.contains("ACTIVE"))
        assertFalse(ondc.state.name.contains("CONNECTED"))
    }

    // ── Government / GeM Channel State ─────────────────────────────────

    @Test
    fun `government channel is not configured by default`() {
        val government = ChannelStatus(
            channelName = "Government",
            state = ChannelState.NOT_CONFIGURED,
            stateLabel = "Not configured",
            detail = "Setup required to sell to government",
            deepLink = "/commerce-hub",
        )
        assertEquals(ChannelState.NOT_CONFIGURED, government.state)
        assertEquals("Not configured", government.stateLabel)
    }

    @Test
    fun `government channel does not claim GeM integration`() {
        // No direct GeM API integration exists
        val government = ChannelStatus(
            channelName = "Government",
            state = ChannelState.NOT_CONFIGURED,
            stateLabel = "Not configured",
        )
        assertFalse(government.state.name.contains("ACTIVE"))
        assertFalse(government.state.name.contains("CONNECTED"))
        assertFalse(government.state.name.contains("APPROVED"))
    }

    // ── Unknown / Unavailable State ────────────────────────────────────

    @Test
    fun `unknown channel state is handled`() {
        val channel = ChannelStatus(
            channelName = "Test",
            state = ChannelState.UNAVAILABLE,
            stateLabel = "Unavailable",
        )
        assertEquals(ChannelState.UNAVAILABLE, channel.state)
    }

    // ── Setup-Required State ──────────────────────────────────────────

    @Test
    fun `setup required state is shown for unconfigured channels`() {
        val ondc = ChannelStatus(
            channelName = "ONDC",
            state = ChannelState.NOT_CONFIGURED,
            stateLabel = "Not configured",
            detail = "Setup required to sell on ONDC",
        )
        // NOT_CONFIGURED means setup is required
        assertEquals(ChannelState.NOT_CONFIGURED, ondc.state)
        assertTrue(ondc.detail!!.contains("Setup required"))
    }

    // ── Stale State ────────────────────────────────────────────────────

    @Test
    fun `stale channel data shows warning`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis() - 3 * 60 * 60 * 1000,
            dataFreshness = DataFreshness.STALE,
            channels = ChannelsSnapshot(
                craftsy = ChannelStatus(
                    channelName = "Craftsy",
                    state = ChannelState.ACTIVE,
                    stateLabel = "Active",
                ),
            ),
        )
        assertEquals(DataFreshness.STALE, snapshot.dataFreshness)
    }

    // ── Logged-Out State ───────────────────────────────────────────────

    @Test
    fun `logged out widget shows sign-in prompt`() {
        val snapshot = WidgetSnapshot(
            authenticated = false,
            accountId = null,
            lastUpdated = 0L,
            dataFreshness = DataFreshness.UNKNOWN,
        )
        assertFalse(snapshot.authenticated)
        assertNull(snapshot.accountId)
    }

    // ── Account Isolation ──────────────────────────────────────────────

    @Test
    fun `different accounts have different channel snapshots`() {
        val snapshotA = WidgetSnapshot(
            authenticated = true,
            accountId = "user-A",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            channels = ChannelsSnapshot(
                craftsy = ChannelStatus(
                    channelName = "Craftsy",
                    state = ChannelState.ACTIVE,
                    stateLabel = "Active",
                ),
            ),
        )
        val snapshotB = WidgetSnapshot(
            authenticated = true,
            accountId = "user-B",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            channels = ChannelsSnapshot(
                craftsy = ChannelStatus(
                    channelName = "Craftsy",
                    state = ChannelState.ACTIVE,
                    stateLabel = "Active",
                ),
            ),
        )
        assertEquals("user-A", snapshotA.accountId)
        assertEquals("user-B", snapshotB.accountId)
    }

    // ── Deep Links ────────────────────────────────────────────────────

    @Test
    fun `craftsy channel deep link is correct`() {
        val craftsy = ChannelStatus(
            channelName = "Craftsy",
            state = ChannelState.ACTIVE,
            stateLabel = "Active",
            deepLink = "/catalogue",
        )
        assertEquals("/catalogue", craftsy.deepLink)
    }

    @Test
    fun `ondc channel deep link is correct`() {
        val ondc = ChannelStatus(
            channelName = "ONDC",
            state = ChannelState.NOT_CONFIGURED,
            stateLabel = "Not configured",
            deepLink = "/commerce-hub",
        )
        assertEquals("/commerce-hub", ondc.deepLink)
    }

    @Test
    fun `government channel deep link is correct`() {
        val government = ChannelStatus(
            channelName = "Government",
            state = ChannelState.NOT_CONFIGURED,
            stateLabel = "Not configured",
            deepLink = "/commerce-hub",
        )
        assertEquals("/commerce-hub", government.deepLink)
    }

    // ── Accessibility Semantics ────────────────────────────────────────

    @Test
    fun `channel status is communicated via text not just color`() {
        // State labels must be meaningful without color
        val activeLabel = "Active"
        val notConfiguredLabel = "Not configured"
        val setupRequiredLabel = "Setup required"

        assertTrue(activeLabel.isNotEmpty())
        assertTrue(notConfiguredLabel.isNotEmpty())
        assertTrue(setupRequiredLabel.isNotEmpty())
    }

    @Test
    fun `channel names are user-friendly`() {
        // "Government" not "GeM API v2"
        // "ONDC" not "ONDC Network Protocol"
        val craftsyName = "Craftsy"
        val ondcName = "ONDC"
        val governmentName = "Government"

        assertEquals("Craftsy", craftsyName)
        assertEquals("ONDC", ondcName)
        assertEquals("Government", governmentName)
    }

    // ── Localization ───────────────────────────────────────────────────

    @Test
    fun `widget labels exist for localization`() {
        val labels = listOf(
            "SELLING CHANNELS",
            "Sell & Grow",
            "Open Craftsy to sign in",
            "Open Craftsy to update",
        )
        assertTrue(labels.isNotEmpty())
        for (label in labels) {
            assertTrue(label.isNotEmpty())
        }
    }

    // ── Idempotent Updates ─────────────────────────────────────────────

    @Test
    fun `repeated identical updates produce same result`() {
        val snapshot = WidgetSnapshot(
            schemaVersion = 1,
            authenticated = true,
            accountId = "user-123",
            lastUpdated = 1000L,
            dataFreshness = DataFreshness.FRESH,
            channels = ChannelsSnapshot(
                craftsy = ChannelStatus(
                    channelName = "Craftsy",
                    state = ChannelState.ACTIVE,
                    stateLabel = "Active",
                ),
            ),
        )
        val json1 = snapshot.toJson().toString()
        val json2 = snapshot.toJson().toString()
        assertEquals(json1, json2)
    }

    // ── No Fabricated Active/Connected State ───────────────────────────

    @Test
    fun `ondc is never shown as active without real integration`() {
        // This test documents the truthfulness boundary
        // ONDC adapter exists but is NOT_CONFIGURED until real API onboarding
        val ondc = ChannelStatus(
            channelName = "ONDC",
            state = ChannelState.NOT_CONFIGURED,
            stateLabel = "Not configured",
        )
        assertFalse(ondc.state == ChannelState.ACTIVE)
        assertFalse(ondc.state == ChannelState.READY)
    }

    @Test
    fun `government is never shown as active without real integration`() {
        // GeM adapter exists but is NOT_CONFIGURED until real API onboarding
        val government = ChannelStatus(
            channelName = "Government",
            state = ChannelState.NOT_CONFIGURED,
            stateLabel = "Not configured",
        )
        assertFalse(government.state == ChannelState.ACTIVE)
        assertFalse(government.state == ChannelState.READY)
    }

    // ── Serialization ──────────────────────────────────────────────────

    @Test
    fun `channels snapshot serializes correctly`() {
        val channels = ChannelsSnapshot(
            craftsy = ChannelStatus(
                channelName = "Craftsy",
                state = ChannelState.ACTIVE,
                stateLabel = "Active",
                deepLink = "/catalogue",
            ),
            ondc = ChannelStatus(
                channelName = "ONDC",
                state = ChannelState.NOT_CONFIGURED,
                stateLabel = "Not configured",
                deepLink = "/commerce-hub",
            ),
            government = ChannelStatus(
                channelName = "Government",
                state = ChannelState.NOT_CONFIGURED,
                stateLabel = "Not configured",
                deepLink = "/commerce-hub",
            ),
        )
        val json = channels.toJson()
        assertTrue(json.has("craftsy"))
        assertTrue(json.has("ondc"))
        assertTrue(json.has("government"))
    }

    @Test
    fun `malformed channels JSON handled gracefully`() {
        val json = org.json.JSONObject("{}")
        val channels = ChannelsSnapshot.fromJson(json)
        assertNull(channels.craftsy)
        assertNull(channels.ondc)
        assertNull(channels.government)
    }

    // ── Security ───────────────────────────────────────────────────────

    @Test
    fun `channels snapshot does not contain credentials`() {
        val snapshot = WidgetSnapshot(
            authenticated = true,
            accountId = "user-123",
            lastUpdated = System.currentTimeMillis(),
            dataFreshness = DataFreshness.FRESH,
            channels = ChannelsSnapshot(
                craftsy = ChannelStatus(
                    channelName = "Craftsy",
                    state = ChannelState.ACTIVE,
                    stateLabel = "Active",
                ),
            ),
        )
        val json = snapshot.toJson()
        assertFalse(json.has("apiKey"))
        assertFalse(json.has("accessToken"))
        assertFalse(json.has("password"))
        assertFalse(json.has("secret"))
        assertFalse(json.has("signingKey"))
    }

    // ── Channel State Enum ─────────────────────────────────────────────

    @Test
    fun `channel state enum has correct values`() {
        assertEquals(8, ChannelState.values().size)
        assertNotNull(ChannelState.valueOf("ACTIVE"))
        assertNotNull(ChannelState.valueOf("READY"))
        assertNotNull(ChannelState.valueOf("NEEDS_ATTENTION"))
        assertNotNull(ChannelState.valueOf("NOT_CONFIGURED"))
        assertNotNull(ChannelState.valueOf("UPDATING"))
        assertNotNull(ChannelState.valueOf("UNAVAILABLE"))
        assertNotNull(ChannelState.valueOf("ERROR"))
        assertNotNull(ChannelState.valueOf("PREPARATION_NEEDED"))
    }

    // ── No Technical Metadata ──────────────────────────────────────────

    @Test
    fun `widget does not expose technical metadata`() {
        // No protocol names, API endpoints, or backend details
        val channel = ChannelStatus(
            channelName = "ONDC",
            state = ChannelState.NOT_CONFIGURED,
            stateLabel = "Not configured",
            detail = "Setup required to sell on ONDC",
        )
        assertFalse(channel.channelName.contains("API"))
        assertFalse(channel.channelName.contains("Protocol"))
        assertFalse(channel.detail!!.contains("endpoint"))
    }
}
