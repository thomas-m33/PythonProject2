const CACHE_NAME = "blog-v1";
const URLS_TO_CACHE = [
  "/", // homepage
  "/about/",
  ];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(URLS_TO_CACHE))
  );
});

  // only use cache for the pages in URLS_TO_CACHE
  if (url.origin === location.origin && URLS_TO_CACHE.includes(url.pathname)) {
    event.respondWith(
      caches.match(event.request).then(response => response || fetch(event.request))
    );
  } else {
    // everything else just fetch from network
    event.respondWith(fetch(event.request));

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    )
  );
});

// pages for specific posts are not cached because it was causing too many issues
// for example if you had a private post in your cache, you could view it even once you signed out
// cache could probably be cleared on logout but i couldn't get it to work
// you can still see a list of posts on the homepage