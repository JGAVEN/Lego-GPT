import { useRef, useEffect } from "react";
import type { WebGLRenderer, Scene, PerspectiveCamera, Group } from "three";

interface Props {
  url: string;
}

export default function LDrawViewer({ url }: Props) {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!mountRef.current) return;

    const mount = mountRef.current;

    /** Alias so WebGLRenderer satisfies the SimpleRenderer expectation  */
    type SimpleRenderer = WebGLRenderer;

    let renderer: SimpleRenderer | null = null;
    let controls:
      | { update: () => void; dispose: () => void; enableDamping: boolean }
      | null = null;
    let animationId: number;

    async function init() {
      /* Dynamic import keeps bundle slim; type-only import above
         provides compile-time safety. */
      const THREE = (await import(
        /* @vite-ignore */
        "https://unpkg.com/three@0.160.0/build/three.module.js?module"
      )) as typeof import("three");

      const { LDrawLoader } = (await import(
        /* @vite-ignore */
        "https://unpkg.com/three@0.160.0/examples/jsm/loaders/LDrawLoader.js?module"
      )) as typeof import("three/examples/jsm/loaders/LDrawLoader.js");

      const { OrbitControls } = (await import(
        /* @vite-ignore */
        "https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js?module"
      )) as typeof import("three/examples/jsm/controls/OrbitControls.js");

      /* Scene setup -------------------------------------------------------- */
      const scene: Scene = new THREE.Scene();

      const camera: PerspectiveCamera = new THREE.PerspectiveCamera(
        45,
        mount.clientWidth / 400,
        1,
        2000
      );
      camera.position.set(200, 200, 200);
      camera.lookAt(0, 0, 0);

      const localRenderer = new THREE.WebGLRenderer({ antialias: true });
      localRenderer.setSize(mount.clientWidth, 400);
      mount.appendChild(localRenderer.domElement);
      renderer = localRenderer;

      const localControls = new OrbitControls(camera, localRenderer.domElement);
      localControls.enableDamping = true;
      controls = localControls;

      /* Load and display LDraw model -------------------------------------- */
      const loader = new LDrawLoader();
      loader.load(url, (group: Group) => {
        scene.add(group);
        animate();
      });

      /* Animation loop ----------------------------------------------------- */
      function animate() {
        animationId = requestAnimationFrame(animate);
        controls?.update();
        renderer?.render(scene, camera);
      }
    }

    init();

    /* Cleanup -------------------------------------------------------------- */
    return () => {
      controls?.dispose();
      if (renderer) {
        renderer.dispose();
        mount.removeChild(renderer.domElement);
      }
      if (animationId) cancelAnimationFrame(animationId);
    };
  }, [url]);

  return <div ref={mountRef} style={{ width: "100%", height: 400 }} />;
}
