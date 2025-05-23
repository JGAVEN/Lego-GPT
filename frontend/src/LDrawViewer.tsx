import { useRef, useEffect } from "react";

interface Props {
  url: string;
}

export default function LDrawViewer({ url }: Props) {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!mountRef.current) return;

    const mount = mountRef.current;

    interface SimpleRenderer {
      domElement: HTMLElement;
      setSize: (width: number, height: number) => void;
      render: (scene: unknown, camera: unknown) => void;
      dispose: () => void;
    }

    let renderer: SimpleRenderer | null = null;
    let animationId: number;

    async function init() {
      const THREE = await import(
        /* @vite-ignore */
        "https://unpkg.com/three@0.160.0/build/three.module.js?module"
      );
      const { LDrawLoader } = await import(
        /* @vite-ignore */
        "https://unpkg.com/three@0.160.0/examples/jsm/loaders/LDrawLoader.js?module"
      );

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(
        45,
        mountRef.current!.clientWidth / 400,
        1,
        2000
      );
      camera.position.set(200, 200, 200);
      camera.lookAt(0, 0, 0);

      renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(mountRef.current!.clientWidth, 400);
      mountRef.current!.appendChild(renderer.domElement);

      const loader = new LDrawLoader();
      loader.load(url, (group: unknown) => {
        // The loaded object is compatible with THREE.Object3D
        (scene as { add: (obj: unknown) => void }).add(group);
        animate();
      });

      function animate() {
        animationId = requestAnimationFrame(animate);
        renderer.render(scene, camera);
      }
    }

      init();
      return () => {
        if (renderer) {
          renderer.dispose();
        }
        if (animationId) {
          cancelAnimationFrame(animationId);
        }
        if (renderer) {
          mount.removeChild(renderer.domElement);
        }
      };
  }, [url]);

  return <div ref={mountRef} style={{ width: "100%", height: 400 }} />;
}
