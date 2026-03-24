/**
 * Three.js floating particles background for auth pages.
 * Soft, slow-moving connected particles with a gentle glow.
 */
(function () {
    const canvas = document.getElementById("bg-canvas");
    if (!canvas) return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 300;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // --- Particles ---
    const PARTICLE_COUNT = 120;
    const SPREAD = 500;
    const positions = new Float32Array(PARTICLE_COUNT * 3);
    const velocities = [];
    const colors = new Float32Array(PARTICLE_COUNT * 3);

    const accentCyan = new THREE.Color(0x00d4ff);
    const accentPurple = new THREE.Color(0x7c3aed);
    const softWhite = new THREE.Color(0x8899aa);

    for (let i = 0; i < PARTICLE_COUNT; i++) {
        positions[i * 3] = (Math.random() - 0.5) * SPREAD;
        positions[i * 3 + 1] = (Math.random() - 0.5) * SPREAD;
        positions[i * 3 + 2] = (Math.random() - 0.5) * SPREAD * 0.5;

        velocities.push({
            x: (Math.random() - 0.5) * 0.15,
            y: (Math.random() - 0.5) * 0.15,
            z: (Math.random() - 0.5) * 0.05,
        });

        const pick = Math.random();
        const color = pick < 0.35 ? accentCyan : pick < 0.65 ? accentPurple : softWhite;
        colors[i * 3] = color.r;
        colors[i * 3 + 1] = color.g;
        colors[i * 3 + 2] = color.b;
    }

    const particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));

    const particleMaterial = new THREE.PointsMaterial({
        size: 2.5,
        vertexColors: true,
        transparent: true,
        opacity: 0.7,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    // --- Lines between nearby particles ---
    const LINE_DISTANCE = 100;
    const lineGeometry = new THREE.BufferGeometry();
    const maxLines = PARTICLE_COUNT * 6;
    const linePositions = new Float32Array(maxLines * 6);
    const lineColors = new Float32Array(maxLines * 6);
    lineGeometry.setAttribute("position", new THREE.BufferAttribute(linePositions, 3));
    lineGeometry.setAttribute("color", new THREE.BufferAttribute(lineColors, 3));

    const lineMaterial = new THREE.LineBasicMaterial({
        vertexColors: true,
        transparent: true,
        opacity: 0.25,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
    });

    const lines = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(lines);

    // --- Mouse interaction ---
    const mouse = { x: 0, y: 0 };
    document.addEventListener("mousemove", (e) => {
        mouse.x = (e.clientX / window.innerWidth - 0.5) * 2;
        mouse.y = -(e.clientY / window.innerHeight - 0.5) * 2;
    });

    // --- Animate ---
    function animate() {
        requestAnimationFrame(animate);

        const pos = particleGeometry.attributes.position.array;

        for (let i = 0; i < PARTICLE_COUNT; i++) {
            pos[i * 3] += velocities[i].x;
            pos[i * 3 + 1] += velocities[i].y;
            pos[i * 3 + 2] += velocities[i].z;

            // Wrap around edges
            if (pos[i * 3] > SPREAD / 2) pos[i * 3] = -SPREAD / 2;
            if (pos[i * 3] < -SPREAD / 2) pos[i * 3] = SPREAD / 2;
            if (pos[i * 3 + 1] > SPREAD / 2) pos[i * 3 + 1] = -SPREAD / 2;
            if (pos[i * 3 + 1] < -SPREAD / 2) pos[i * 3 + 1] = SPREAD / 2;
        }

        particleGeometry.attributes.position.needsUpdate = true;

        // Update lines
        let lineIdx = 0;
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            for (let j = i + 1; j < PARTICLE_COUNT; j++) {
                const dx = pos[i * 3] - pos[j * 3];
                const dy = pos[i * 3 + 1] - pos[j * 3 + 1];
                const dz = pos[i * 3 + 2] - pos[j * 3 + 2];
                const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

                if (dist < LINE_DISTANCE && lineIdx < maxLines) {
                    const alpha = 1 - dist / LINE_DISTANCE;

                    linePositions[lineIdx * 6] = pos[i * 3];
                    linePositions[lineIdx * 6 + 1] = pos[i * 3 + 1];
                    linePositions[lineIdx * 6 + 2] = pos[i * 3 + 2];
                    linePositions[lineIdx * 6 + 3] = pos[j * 3];
                    linePositions[lineIdx * 6 + 4] = pos[j * 3 + 1];
                    linePositions[lineIdx * 6 + 5] = pos[j * 3 + 2];

                    lineColors[lineIdx * 6] = 0 * alpha;
                    lineColors[lineIdx * 6 + 1] = 0.83 * alpha;
                    lineColors[lineIdx * 6 + 2] = 1 * alpha;
                    lineColors[lineIdx * 6 + 3] = 0.49 * alpha;
                    lineColors[lineIdx * 6 + 4] = 0.23 * alpha;
                    lineColors[lineIdx * 6 + 5] = 0.93 * alpha;

                    lineIdx++;
                }
            }
        }

        lineGeometry.setDrawRange(0, lineIdx * 2);
        lineGeometry.attributes.position.needsUpdate = true;
        lineGeometry.attributes.color.needsUpdate = true;

        // Gentle camera sway following mouse
        camera.position.x += (mouse.x * 30 - camera.position.x) * 0.02;
        camera.position.y += (mouse.y * 30 - camera.position.y) * 0.02;
        camera.lookAt(scene.position);

        renderer.render(scene, camera);
    }

    animate();

    // --- Resize ---
    window.addEventListener("resize", () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
})();
