package com.ymcx.predirecta

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.browser.customtabs.CustomTabsIntent

class MainActivity : AppCompatActivity() {
    override fun onCreate(bundle: Bundle?) {
        super.onCreate(bundle)
        val prefs = getPreferences(MODE_PRIVATE)
        val prefsInstance = getString(R.string.instance)
        var url = prefs.getString(prefsInstance, "redirect.invidious.io")
        when (intent.action) {
            Intent.ACTION_SEND -> {
                url = intent.getStringExtra(Intent.EXTRA_TEXT).orEmpty()
                    .replace("\"", "")
                    .replace("http://", "")
                    .replace("https://", "")
                    .split("/")[0]
                with (prefs.edit()) {
                    putString(prefsInstance, url)
                    apply()
                }
            }
            Intent.ACTION_VIEW -> {
                url = intent.getData().toString()
                    .replace(Regex("(.*)youtube.com/"), url+"/")
                    .replace(Regex("(.*)youtu.be/"),    url+"/watch?v=")
            }
        }
        CustomTabsIntent.Builder().build().launchUrl(this, Uri.parse("https://"+url))
        finish()
    }
}
