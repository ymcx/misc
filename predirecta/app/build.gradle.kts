plugins {
    id("com.android.application")
    kotlin("android")
}

android {
    namespace = "com.ymcx.predirecta"
    compileSdk = 35
    defaultConfig {
        minSdk = 34
        targetSdk = 35
    }
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"))
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_21
        targetCompatibility = JavaVersion.VERSION_21
    }
    kotlinOptions {
        jvmTarget = "21"
    }
}

dependencies {
    implementation("com.google.android.material:material:+")
    implementation("androidx.browser:browser:+")
}
