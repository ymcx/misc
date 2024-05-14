package com.ymcx.predirecta

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.app.AlertDialog
import android.content.SharedPreferences
import android.widget.EditText
import androidx.browser.customtabs.CustomTabsIntent

class MainActivity : AppCompatActivity() {
    lateinit var sharedPref: SharedPreferences
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        sharedPref = getPreferences(MODE_PRIVATE)
        if (intent?.action == Intent.ACTION_VIEW) {
            val oldUrl = intent.data.toString()
            val address = sharedPref.getString(getString(R.string.url), null)
            val parameters = oldUrl.substring(oldUrl.lastIndexOf('/'), oldUrl.length)
            val url = Uri.parse("https://" + address + parameters)
            CustomTabsIntent.Builder().setShareState(2).build().launchUrl(this, url)
            finish()
        }
        else {
            val builder = AlertDialog.Builder(this)
            builder.apply {
                val input = EditText(context)
                builder.setView(input)
                setPositiveButton("Save") { _, _ ->
                    with(sharedPref.edit()) {
                        putString(getString(R.string.url), input.text.toString())
                        apply()
                    }
                    finish()
                }
            }
            builder.show()
        }
    }
}
