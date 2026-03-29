const CACHE_NAME = "blog-v1";
const URLS_TO_CACHE = [
  "/", // home page
  "/about/",
  ];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(URLS_TO_CACHE))
  );
});

self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);

  // try load through network first, fallback to cache
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    )
  );
});

// post pages are not cached because it was causing too many issues
// for example if you had a private post in your cache, you could view it even once you signed out
// cache could probably be cleared on logout but i couldn't get it to work