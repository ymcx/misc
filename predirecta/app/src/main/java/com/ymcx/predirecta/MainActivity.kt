package com.ymcx.predirecta

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.browser.customtabs.CustomTabsIntent

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val prefs = getPreferences(MODE_PRIVATE)
        val instance = getString(R.string.instance)
        if (intent.action == Intent.ACTION_SEND) {
            val newInstance = intent.getStringExtra(Intent.EXTRA_TEXT)
            val prefsEdit = prefs.edit()
            prefsEdit.putString(instance, newInstance)
            prefsEdit.apply()
        }
        else {
            val url = intent.data.toString()
            val instance = prefs.getString(instance, null)
            val prefix = if (url.startsWith("https://youtu.be", true)) {"watch?v="} else {""}
            val parameters = url.substring(url.lastIndexOf('/')+1, url.length)
            val newUrl = Uri.parse(instance + prefix + parameters)
            CustomTabsIntent.Builder().build().launchUrl(this, newUrl)
        }
        finish()
    }
}
