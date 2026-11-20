// Optional enhancement. The page is complete without this file: it ships with a
// committed fallback photo. This swaps in a fresh public-domain photo from
// Wikimedia Commons, once per browser session. Any failure leaves the fallback.
(function () {
  var img = document.querySelector(".bg");
  var conn = navigator.connection;
  if (!img || !window.fetch || (conn && conn.saveData)) return;

  var TITLES = [
    "File:Chuttersnap 2016-09-12 (Unsplash 2PD0nAkzkjo).jpg",
    "File:Cumulus congestus over Gåseberg 3-bw.jpg",
    "File:Forest road Slavne 2017 BW G3.jpg",
    "File:Forest road Slavne 2017 BW G6.jpg",
    "File:Light rays in a foggy forest (55092954957).jpg",
    "File:Maria's lookout.jpg",
    "File:Monochrome road in hills (Unsplash).jpg",
    "File:Monochrome snowy mountains (Unsplash).jpg",
    "File:Mount McKinley (6473166469).jpg",
    "File:Mountainous train ride (Unsplash).jpg",
    "File:Scuol-Motta Naluns, 15-09-2023. (actm.) 05.jpg",
    "File:Scuol-Motta Naluns, 15-09-2023. (actm.) 11.jpg",
    "File:Storm Clouds Black White (Unsplash).jpg",
    "File:Tomek Kaczmarek 2016 (Unsplash).jpg"
  ];
  var STEPS = [960, 1280, 1920];
  var KEY = "bg";

  function width() {
    var want = Math.max(window.innerWidth, window.innerHeight * 0.75) * (window.devicePixelRatio || 1);
    for (var i = 0; i < STEPS.length; i++) if (STEPS[i] >= want) return STEPS[i];
    return STEPS[STEPS.length - 1];
  }

  function show(url) {
    var probe = new Image();
    probe.referrerPolicy = "no-referrer";
    probe.onload = function () {
      img.removeAttribute("srcset");
      img.removeAttribute("sizes");
      img.src = url;
    };
    probe.src = url;
  }

  function ok(url) {
    try {
      var h = new URL(url).hostname;
      return h === "upload.wikimedia.org" || h === "thumb.wikimedia.org";
    } catch (e) { return false; }
  }

  var cached;
  try { cached = sessionStorage.getItem(KEY); } catch (e) {}
  if (cached && ok(cached)) { show(cached); return; }

  var title = TITLES[Math.floor(Math.random() * TITLES.length)];
  var query = "https://commons.wikimedia.org/w/api.php?action=query&format=json&formatversion=2&origin=*" +
    "&prop=imageinfo&iiprop=url&iiurlwidth=" + width() + "&titles=" + encodeURIComponent(title);

  fetch(query, { referrerPolicy: "no-referrer" })
    .then(function (r) { return r.ok ? r.json() : Promise.reject(); })
    .then(function (data) {
      var info = data.query.pages[0].imageinfo[0];
      var url = info.thumburl || info.url;
      if (!ok(url)) return;
      try { sessionStorage.setItem(KEY, url); } catch (e) {}
      show(url);
    })
    .catch(function () {});
})();
