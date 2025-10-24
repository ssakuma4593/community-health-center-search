"use client";

import Link from "next/link";

export default function Navigation() {
  return (
    <nav className="bg-white shadow-sm border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold text-gray-900">
            Sphere AI
          </Link>
          <div className="space-x-4">
            <Link 
              href="/" 
              className="text-gray-600 hover:text-gray-900 transition duration-200"
            >
              Health Centers
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
