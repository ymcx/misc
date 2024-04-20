package com.ymcx.predirecta

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.util.Log

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(null)
        val data = intent.data.toString()
        startActivity(Intent(Intent.ACTION_VIEW, Uri.parse("https://yewtu.be" + data.substring(data.lastIndexOf('/'), data.length))))
        finish()
    }
}
