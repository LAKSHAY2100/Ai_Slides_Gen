(function () {
    "use strict";

    function clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    }

    function smoothStep(edge0, edge1, x) {
        const t = clamp((x - edge0) / (edge1 - edge0), 0, 1);
        return t * t * (3 - 2 * t);
    }

    function sectionProgress(section, viewportHeight) {
        const rect = section.getBoundingClientRect();
        const total = Math.max(section.offsetHeight - viewportHeight, 1);
        const traveled = clamp(-rect.top, 0, total);
        return traveled / total;
    }

    function initOverlayNarrative(config) {
        const section = config.section;
        const selector = config.selector || "[data-overlay-step]";
        const steps = Array.prototype.slice.call(document.querySelectorAll(selector));

        if (!section || !steps.length) {
            return;
        }

        let ticking = false;

        function update() {
            ticking = false;
            const progress = sectionProgress(section, window.innerHeight);

            for (let i = 0; i < steps.length; i++) {
                const node = steps[i];
                const start = Number(node.dataset.start || 0);
                const end = Number(node.dataset.end || 1);
                const direction = String(node.dataset.direction || "center");
                const local = clamp((progress - start) / Math.max(end - start, 0.0001), 0, 1);

                const fadeIn = smoothStep(0.0, 0.16, local);
                const fadeOut = 1 - smoothStep(0.74, 1.0, local);
                const opacity = fadeIn * fadeOut;
                const y = (1 - local) * 56 - local * 20;
                const driftBase = (0.5 - local) * 36;
                const x = direction === "left" ? -driftBase : direction === "right" ? driftBase : 0;
                const scale = 0.985 + (opacity * 0.015);

                node.style.opacity = opacity.toFixed(3);
                node.style.transform = "translate3d(" + x.toFixed(1) + "px," + y.toFixed(1) + "px,0) scale(" + scale.toFixed(3) + ")";
            }
        }

        function requestTick() {
            if (!ticking) {
                ticking = true;
                window.requestAnimationFrame(update);
            }
        }

        requestTick();
        window.addEventListener("scroll", requestTick, { passive: true });
        window.addEventListener("resize", requestTick, { passive: true });
    }

    window.initOverlayNarrative = initOverlayNarrative;
})();
