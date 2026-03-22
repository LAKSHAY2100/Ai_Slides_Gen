(function () {
    "use strict";

    function clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    }

    function padFrame(num) {
        return String(num).padStart(3, "0");
    }

    function createFrameUrl(basePath, index, suffix) {
        return basePath + padFrame(index) + suffix;
    }

    function drawCover(ctx, canvas, image) {
        const cw = canvas.clientWidth || window.innerWidth;
        const ch = canvas.clientHeight || window.innerHeight;
        const iw = image.naturalWidth || image.width;
        const ih = image.naturalHeight || image.height;

        if (!iw || !ih) {
            return;
        }

        const scale = Math.max(cw / iw, ch / ih);
        const sw = iw * scale;
        const sh = ih * scale;
        const dx = (cw - sw) * 0.5;
        const dy = (ch - sh) * 0.5;

        ctx.clearRect(0, 0, cw, ch);
        ctx.drawImage(image, dx, dy, sw, sh);
    }

    function preloadImages(frameCount, basePath, suffix) {
        const images = new Array(frameCount);
        let loaded = 0;

        return new Promise(function (resolve) {
            for (let i = 0; i < frameCount; i++) {
                const img = new Image();
                img.decoding = "async";
                img.src = createFrameUrl(basePath, i, suffix);

                img.onload = function () {
                    loaded += 1;
                    images[i] = img;
                    if (loaded === frameCount) {
                        resolve(images);
                    }
                };

                img.onerror = function () {
                    loaded += 1;
                    images[i] = null;
                    if (loaded === frameCount) {
                        resolve(images);
                    }
                };
            }
        });
    }

    function getProgress(section, viewportHeight) {
        const rect = section.getBoundingClientRect();
        const total = Math.max(section.offsetHeight - viewportHeight, 1);
        const traveled = clamp(-rect.top, 0, total);
        return traveled / total;
    }

    function initScrollyCanvas(config) {
        const canvas = config.canvas;
        const section = config.section;
        const loader = config.loader || null;
        const frameCount = config.frameCount || 120;
        const basePath = config.basePath || "";
        const suffix = config.suffix || ".png";
        const scrubEase = clamp(Number(config.scrubEase || 0.14), 0.05, 0.4);

        if (!canvas || !section || !basePath) {
            return;
        }

        const ctx = canvas.getContext("2d", { alpha: false });
        if (!ctx) {
            return;
        }

        let rafId = 0;
        let needsRender = true;
        let currentFrame = -1;
        let targetProgress = 0;
        let currentProgress = 0;
        let images = [];

        function resizeCanvas() {
            const dpr = Math.min(window.devicePixelRatio || 1, 2);
            const width = window.innerWidth;
            const height = window.innerHeight;

            canvas.width = Math.floor(width * dpr);
            canvas.height = Math.floor(height * dpr);
            canvas.style.width = width + "px";
            canvas.style.height = height + "px";

            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            needsRender = true;
        }

        function pickRenderableFrame(frameIndex) {
            if (images[frameIndex]) {
                return images[frameIndex];
            }

            for (let i = frameIndex - 1; i >= 0; i--) {
                if (images[i]) {
                    return images[i];
                }
            }

            for (let i = frameIndex + 1; i < images.length; i++) {
                if (images[i]) {
                    return images[i];
                }
            }

            return null;
        }

        function render() {
            const delta = targetProgress - currentProgress;
            if (Math.abs(delta) > 0.0002) {
                currentProgress += delta * scrubEase;
                needsRender = true;
            } else {
                currentProgress = targetProgress;
            }

            const frameIndex = clamp(Math.round(currentProgress * (frameCount - 1)), 0, frameCount - 1);

            if (needsRender || frameIndex !== currentFrame) {
                const frame = pickRenderableFrame(frameIndex);
                if (frame) {
                    drawCover(ctx, canvas, frame);
                    currentFrame = frameIndex;
                    needsRender = false;
                }
            }

            rafId = window.requestAnimationFrame(render);
        }

        function onScroll() {
            targetProgress = getProgress(section, window.innerHeight);
            needsRender = true;
        }

        function onResize() {
            resizeCanvas();
            onScroll();
        }

        resizeCanvas();
        onScroll();

        preloadImages(frameCount, basePath, suffix).then(function (loadedImages) {
            images = loadedImages;
            if (loader) {
                loader.style.opacity = "0";
                loader.style.pointerEvents = "none";
            }
            needsRender = true;
        });

        window.addEventListener("scroll", onScroll, { passive: true });
        window.addEventListener("resize", onResize, { passive: true });

        if (rafId) {
            window.cancelAnimationFrame(rafId);
        }
        rafId = window.requestAnimationFrame(render);
    }

    window.initScrollyCanvas = initScrollyCanvas;
})();
