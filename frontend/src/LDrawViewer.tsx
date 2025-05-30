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
    let controls: { update: () => void; dispose: () => void; enableDamping: boolean } | null = null;
    let animationId: number;

    async function init() {
      const THREE: any = await import(
        /* @vite-ignore */
        "https://unpkg.com/three@0.160.0/build/three.module.js?module"
      );
      const { LDrawLoader } = (await import(
        /* @vite-ignore */
        "https://unpkg.com/three@0.160.0/examples/jsm/loaders/LDrawLoader.js?module"
      )) as any;

      const scene = new THREE.Scene();
      const camera = new THREE.PerspectiveCamera(
        45,
        mountRef.current!.clientWidth / 400,
        1,
        2000
      );
      camera.position.set(200, 200, 200);
      camera.lookAt(0, 0, 0);

      const { OrbitControls } = (await import(
        /* @vite-ignore */
        "https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js?module"
      )) as any;

      renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer!.setSize(mountRef.current!.clientWidth, 400);
      mountRef.current!.appendChild(renderer!.domElement);

      controls = new OrbitControls(camera, renderer!.domElement);
      controls!.enableDamping = true;

      const loader = new LDrawLoader();
      loader.load(url, (group: unknown) => {
        // The loaded object is compatible with THREE.Object3D
        (scene as { add: (obj: unknown) => void }).add(group);
        animate();
      });

      function animate() {
        animationId = requestAnimationFrame(animate);
        controls?.update();
        renderer!.render(scene, camera);
      }
    }

      init();
      return () => {
        controls?.dispose();
        if (renderer) {
          renderer.dispose();
          mount.removeChild(renderer.domElement);
        }
        if (animationId) {
          cancelAnimationFrame(animationId);
        }
      };
  }, [url]);

  return <div ref={mountRef} style={{ width: "100%", height: 400 }} />;
}
