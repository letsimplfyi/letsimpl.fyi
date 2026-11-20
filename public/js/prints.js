// Optional enhancement. The page is complete without this file: every print
// ships with a committed fallback photo. This swaps each print for a random
// public-domain photo from its pool on Wikimedia Commons, with one API request
// per browser session. Any failure leaves the fallback in place.
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll("img[data-pool]"));
  var conn = navigator.connection;
  if (!imgs.length || !window.fetch || (conn && conn.saveData)) return;

  var KEY = "prints";
  var STEPS = [480, 960, 1280];

  function width() {
    var want = 320 * (window.devicePixelRatio || 1);
    for (var i = 0; i < STEPS.length; i++) if (STEPS[i] >= want) return STEPS[i];
    return STEPS[STEPS.length - 1];
  }

  function ok(url) {
    try {
      var h = new URL(url).hostname;
      return h === "upload.wikimedia.org" || h === "thumb.wikimedia.org";
    } catch (e) { return false; }
  }

  function show(img, url) {
    var probe = new Image();
    probe.referrerPolicy = "no-referrer";
    probe.onload = function () {
      img.removeAttribute("srcset");
      img.removeAttribute("sizes");
      img.src = url;
    };
    probe.src = url;
  }

  function apply(urls) {
    imgs.forEach(function (img, i) { if (urls[i] && ok(urls[i])) show(img, urls[i]); });
  }

  var cached;
  try { cached = JSON.parse(sessionStorage.getItem(KEY)); } catch (e) {}
  if (cached && cached.length === imgs.length) { apply(cached); return; }

  var picks = imgs.map(function (img) {
    var pool = img.getAttribute("data-pool").split("|");
    return pool[Math.floor(Math.random() * pool.length)];
  });
  var query = "https://commons.wikimedia.org/w/api.php?action=query&format=json&formatversion=2&origin=*" +
    "&prop=imageinfo&iiprop=url&iiurlwidth=" + width() + "&titles=" + encodeURIComponent(picks.join("|"));

  fetch(query, { referrerPolicy: "no-referrer" })
    .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
    .then(function (data) {
      var byTitle = {};
      (data.query.normalized || []).forEach(function (n) { byTitle[n.from] = n.to; });
      var pages = {};
      data.query.pages.forEach(function (p) { if (p.imageinfo) pages[p.title] = p.imageinfo[0]; });
      var urls = picks.map(function (t) {
        var info = pages[byTitle[t] || t];
        return info ? (info.thumburl || info.url) : "";
      });
      try { sessionStorage.setItem(KEY, JSON.stringify(urls)); } catch (e) {}
      apply(urls);
    })
    .catch(function () {});
})();
