package com.ymcx.predirecta

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(bundle: Bundle?) {
        super.onCreate(bundle)
        val prefs = getPreferences(MODE_PRIVATE)
        val prefsInstance = getString(R.string.instance)
        val url = intent.getData().toString()
        if (intent.action == Intent.ACTION_SEND) {
            with (prefs.edit()) {
                putString(prefsInstance, url)
                apply()
            }
        }
        else {
            val instance = prefs.getString(prefsInstance, "yewtu.be")
            val newUrl = Uri.parse(url
                .replace(Regex("(.*)youtube.com/"), "https://"+instance+"/")
                .replace(Regex("(.*)youtu.be/"),    "https://"+instance+"/watch?v=")
            )
            startActivity(Intent(Intent.ACTION_VIEW, newUrl))
        }
        finish()
    }
}
