plugins {
    id("com.android.application")
    kotlin("android")
}

android {
    namespace = "com.ymcx.predirecta"
    compileSdk = 34
    defaultConfig {
        minSdk = 34
    }
    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"))
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_22
        targetCompatibility = JavaVersion.VERSION_22
    }
    kotlinOptions {
        jvmTarget = "22"
    }
}

dependencies {
    implementation("com.google.android.material:material:+")
    implementation("androidx.browser:browser:+")
}
