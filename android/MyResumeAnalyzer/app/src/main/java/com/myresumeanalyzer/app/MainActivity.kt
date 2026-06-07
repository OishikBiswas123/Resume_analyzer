package com.myresumeanalyzer.app

import android.annotation.SuppressLint
import android.graphics.Bitmap
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.view.View
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.ProgressBar
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import com.google.android.material.button.MaterialButton

class MainActivity : AppCompatActivity() {

    companion object {
        private const val APP_URL = "https://resumeanalyzer-tdc8xvnbegkgzn6fg5pwmt.streamlit.app"
    }

    private lateinit var webView: WebView
    private lateinit var progressBar: ProgressBar
    private lateinit var swipeRefreshLayout: SwipeRefreshLayout
    private lateinit var errorView: View
    private lateinit var errorText: TextView
    private lateinit var retryButton: MaterialButton
    private val mainHandler = Handler(Looper.getMainLooper())

    // JavaScript to hide Streamlit footer elements robustly (via evaluateJavascript)
    private val footerHidingScript = """
        (function() {
            function hideFooterElements() {
                var allElements = document.querySelectorAll('a, div, footer, span, section, p');
                var found = false;
                for (var i = 0; i < allElements.length; i++) {
                    var el = allElements[i];
                    var text = (el.textContent || el.innerText || '').trim();
                    var html = (el.innerHTML || '').toLowerCase();
                    if (text.indexOf('Hosted with Streamlit') > -1 ||
                        text.indexOf('Created by') > -1 ||
                        html.indexOf('hosted with streamlit') > -1 ||
                        html.indexOf('created by') > -1) {
                        el.style.display = 'none';
                        el.style.visibility = 'hidden';
                        el.style.height = '0px';
                        el.style.overflow = 'hidden';
                        el.setAttribute('hidden', '');
                        found = true;
                    }
                }
                if (found) {
                    console.log('[FooterHider] Found and hid footer elements');
                }
                return found;
            }

            // Run immediately
            hideFooterElements();

            // Run on delays (Streamlit loads content dynamically)
            setTimeout(function() { hideFooterElements(); }, 1000);
            setTimeout(function() { hideFooterElements(); }, 2000);
            setTimeout(function() { hideFooterElements(); }, 3000);
            setTimeout(function() { hideFooterElements(); }, 5000);
            setTimeout(function() { hideFooterElements(); }, 8000);

            // MutationObserver to catch dynamically loaded content
            var targetNode = document.body || document.documentElement;
            if (targetNode) {
                var observer = new MutationObserver(function(mutations) {
                    hideFooterElements();
                });
                observer.observe(targetNode, {
                    childList: true,
                    subtree: true,
                    attributes: false,
                    characterData: false
                });
            }
        })();
    """.trimIndent()

    // JavaScript to hide footer via loadUrl with javascript: scheme (backup)
    private val footerHidingUrl = "javascript:" + """
        (function() {
            function hideFooterElements() {
                var elements = document.querySelectorAll('a, div, footer, span, section, p');
                for (var i = 0; i < elements.length; i++) {
                    var el = elements[i];
                    var text = (el.textContent || el.innerText || '').trim();
                    var html = (el.innerHTML || '').toLowerCase();
                    if (text.indexOf('Hosted with Streamlit') > -1 ||
                        text.indexOf('Created by') > -1 ||
                        html.indexOf('hosted with streamlit') > -1 ||
                        html.indexOf('created by') > -1) {
                        el.style.display = 'none';
                        el.style.visibility = 'hidden';
                        el.style.height = '0px';
                        el.style.overflow = 'hidden';
                        el.setAttribute('hidden', '');
                    }
                }
            }
            hideFooterElements();
            setTimeout(hideFooterElements, 2000);
            setTimeout(hideFooterElements, 5000);
            var o = new MutationObserver(function(){hideFooterElements();});
            o.observe(document.body||document.documentElement, {childList:true,subtree:true});
        })();
    """.trimIndent().replace("\n", "")

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.webView)
        progressBar = findViewById(R.id.progressBar)
        swipeRefreshLayout = findViewById(R.id.swipeRefreshLayout)
        errorView = findViewById(R.id.errorView)
        errorText = findViewById(R.id.errorText)
        retryButton = findViewById(R.id.retryButton)

        configureWebView()
        configureSwipeRefresh()
        configureRetryButton()

        loadAppUrl()
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun configureWebView() {
        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true
            setSupportMultipleWindows(false)
            allowFileAccess = false
            allowContentAccess = false
            useWideViewPort = true
            loadWithOverviewMode = true
            builtInZoomControls = false
            displayZoomControls = false
            setSupportZoom(false)
            userAgentString = "${userAgentString} MyResumeAnalyzer/1.0"
        }

        webView.webViewClient = object : WebViewClient() {
            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                super.onPageStarted(view, url, favicon)
                progressBar.visibility = View.VISIBLE
                errorView.visibility = View.GONE
                webView.visibility = View.GONE
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                progressBar.visibility = View.GONE
                webView.visibility = View.VISIBLE
                swipeRefreshLayout.isRefreshing = false

                // Method 1: evaluateJavascript (modern API)
                injectFooterHidingJS()

                // Method 2: loadUrl with javascript: scheme (backup, runs on delay)
                mainHandler.postDelayed({
                    try {
                        webView.loadUrl(footerHidingUrl)
                    } catch (e: Exception) {
                        // Silently fail - method 1 should work
                    }
                }, 500)

                // Method 3: Repeated injections to catch late-loading content
                mainHandler.postDelayed({
                    injectFooterHidingJS()
                    try { webView.loadUrl(footerHidingUrl) } catch (_: Exception) {}
                }, 3000)

                mainHandler.postDelayed({
                    injectFooterHidingJS()
                    try { webView.loadUrl(footerHidingUrl) } catch (_: Exception) {}
                }, 6000)
            }

            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?
            ) {
                super.onReceivedError(view, request, error)

                if (request?.isForMainFrame == true) {
                    progressBar.visibility = View.GONE
                    webView.visibility = View.GONE
                    errorView.visibility = View.VISIBLE
                    errorText.text = getString(
                        R.string.error_loading,
                        error?.description ?: getString(R.string.unknown_error)
                    )
                }
            }

            override fun shouldOverrideUrlLoading(
                view: WebView?,
                request: WebResourceRequest?
            ): Boolean {
                return false
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                super.onProgressChanged(view, newProgress)
                progressBar.progress = newProgress
            }
        }
    }

    private fun injectFooterHidingJS() {
        try {
            webView.evaluateJavascript(footerHidingScript, null)
        } catch (e: Exception) {
            // Fallback to loadUrl method
            try {
                webView.loadUrl(footerHidingUrl)
            } catch (_: Exception) {}
        }
    }

    private fun configureSwipeRefresh() {
        swipeRefreshLayout.setOnRefreshListener {
            errorView.visibility = View.GONE
            webView.visibility = View.VISIBLE
            loadAppUrl()
        }
        swipeRefreshLayout.setColorSchemeResources(
            android.R.color.holo_blue_dark,
            android.R.color.holo_green_dark,
            android.R.color.holo_orange_dark
        )
    }

    private fun configureRetryButton() {
        retryButton.setOnClickListener {
            errorView.visibility = View.GONE
            progressBar.visibility = View.VISIBLE
            loadAppUrl()
        }
    }

    private fun loadAppUrl() {
        webView.loadUrl(APP_URL)
    }

    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        mainHandler.removeCallbacksAndMessages(null)
    }
}
