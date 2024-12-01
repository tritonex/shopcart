self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open("v1").then((cache) => {
      return cache.addAll([
        "/",
        "/auth/login",
        "/static/manifest.json",
        "/static/cart192.png",
        "/static/cart512.png",
      ]);
    })
  );
});
