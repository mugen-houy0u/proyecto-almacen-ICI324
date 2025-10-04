// src/components/LoginForm.tsx
import { useState } from "preact/hooks";

export default function LoginForm() {
  const [role, setRole] = useState<"operador" | "admin">("operador");

  return (
    <div class="flex flex-col items-center justify-center min-h-screen bg-[url('/bg.jpg')] bg-cover">
      {/* Switch de roles */}
      <div class="flex mb-6 rounded-lg shadow-md overflow-hidden">
        <button
          class={`px-6 py-2 font-medium transition ${
            role === "operador"
              ? "bg-white text-black"
              : "bg-black text-white hover:bg-gray-800"
          }`}
          onClick={() => setRole("operador")}
        >
          Operador
        </button>
        <button
          class={`px-6 py-2 font-medium transition ${
            role === "admin"
              ? "bg-white text-black"
              : "bg-black text-white hover:bg-gray-800"
          }`}
          onClick={() => setRole("admin")}
        >
          Admin
        </button>
      </div>

      {/* Card del login */}
      <div class="w-80 p-6 rounded-xl shadow-xl bg-white/30 backdrop-blur-md border border-white/40">
        <form class="flex flex-col gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-900">Email</label>
            <input
              type="email"
              placeholder="Value"
              class="mt-1 w-full rounded-lg px-3 py-2 bg-white/80 text-black focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-900">Password</label>
            <input
              type="password"
              placeholder="Value"
              class="mt-1 w-full rounded-lg px-3 py-2 bg-white/80 text-black focus:outline-none focus:ring-2 focus:ring-black"
            />
          </div>

          <button
            type="submit"
            class="mt-2 w-full bg-black text-white font-semibold py-2 rounded-lg hover:bg-gray-800 transition"
          >
            Sign In
          </button>
        </form>

        <div class="mt-4 text-center">
          <a href="#" class="text-sm text-black underline hover:text-gray-700">
            Forgot password?
          </a>
        </div>
      </div>
    </div>
  );
}
