package com.ymcx.predirecta

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.browser.customtabs.CustomTabsIntent

class MainActivity : AppCompatActivity() {
    fun openUrl(url: String) {
        CustomTabsIntent.Builder().build().launchUrl(this, Uri.parse(url))
    }
    override fun onCreate(bundle: Bundle?) {
        super.onCreate(bundle)
        val prefs = getPreferences(MODE_PRIVATE)
        val prefsInstance = getString(R.string.instance)
        val instance = prefs.getString(prefsInstance, "redirect.invidious.io").orEmpty().replace(" ", "")
        when (intent.action) {
            Intent.ACTION_SEND -> {
                val url = intent.getStringExtra(Intent.EXTRA_TEXT).orEmpty()
                    .replace(Regex("(\"|https://|http://|/.*)"), "")
                with (prefs.edit()) {
                    putString(prefsInstance, url)
                    apply()
                }
            }
            Intent.ACTION_VIEW -> {
                val url = intent.getData().toString()
                    .replace(Regex("(m.youtube.com|www.youtube.com|youtube.com|youtu.be)"), instance)
                openUrl(url)
            }
        }
        finish()
    }
}
