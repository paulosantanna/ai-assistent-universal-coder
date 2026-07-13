pluginManagement {
    repositories {
        gradlePluginPortal()
        maven {
            url = uri("https://repo1.maven.org/maven2")
        }
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        maven {
            url = uri("https://repo1.maven.org/maven2")
        }
    }
}

rootProject.name = "aeos-gradle-junit5-template"
