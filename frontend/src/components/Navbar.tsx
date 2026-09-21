"use client";

import React from "react";
import { Sprout, Leaf, FlaskConical, BarChart3, ShieldCheck, Grid3X3, GraduationCap } from "lucide-react";

export type TabKey = "crop" | "fertilizer" | "analytics" | "critical" | "expdesign" | "viva";

interface NavbarProps {
  activeTab: TabKey;
  setActiveTab: (tab: TabKey) => void;
  isBackendOnline: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab, isBackendOnline }) => {
  const navItems: { key: TabKey; label: string; icon: React.ReactNode }[] = [
    { key: "crop", label: "Crop Predictor", icon: <Leaf className="w-4 h-4" /> },
    { key: "fertilizer", label: "Fertilizer Advisor", icon: <FlaskConical className="w-4 h-4" /> },
    { key: "analytics", label: "Analytics & EDA", icon: <BarChart3 className="w-4 h-4" /> },
    { key: "critical", label: "Critical Thinking", icon: <ShieldCheck className="w-4 h-4" /> },
    { key: "expdesign", label: "Experimental Design", icon: <Grid3X3 className="w-4 h-4" /> },
    { key: "viva", label: "Teacher Viva Guide", icon: <GraduationCap className="w-4 h-4" /> },
  ];

  return (
    <header className="sticky top-0 z-40 bg-obsidian-950/80 backdrop-blur-xl border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Simple Brand Header */}
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-emerald-400 flex items-center justify-center shadow-emerald-glow">
            <Sprout className="w-5 h-5 text-black stroke-[2.5]" />
          </div>
          <div>
            <h1 className="font-sans font-bold text-lg tracking-tight text-white flex items-center gap-1.5">
              Crop &amp; Fertilizer <span className="text-emerald-400">ML</span>
            </h1>
          </div>
        </div>

        {/* Desktop Tab Navigation */}
        <nav className="hidden md:flex items-center space-x-1 bg-obsidian-900 p-1 rounded-xl border border-white/10">
          {navItems.map((item) => {
            const isActive = activeTab === item.key;
            return (
              <button
                key={item.key}
                onClick={() => setActiveTab(item.key)}
                className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all duration-200 ${
                  isActive
                    ? "bg-emerald-500 text-black font-semibold shadow-emerald-glow"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                }`}
              >
                {item.icon}
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* Backend Status Badge */}
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-2 text-xs font-mono px-3 py-1.5 rounded-lg bg-obsidian-900 border border-white/10">
            <span
              className={`w-2 h-2 rounded-full ${
                isBackendOnline ? "bg-emerald-400 animate-pulse" : "bg-amber-400"
              }`}
            />
            <span className="text-slate-300 hidden sm:inline">
              {isBackendOnline ? "ML Engine Online" : "Local Standalone"}
            </span>
          </div>
        </div>
      </div>

      {/* Mobile Tab Scroll Bar */}
      <div className="md:hidden flex overflow-x-auto px-4 py-2 space-x-1.5 border-t border-white/5 bg-obsidian-900">
        {navItems.map((item) => (
          <button
            key={item.key}
            onClick={() => setActiveTab(item.key)}
            className={`flex items-center space-x-1.5 px-3 py-1 text-xs whitespace-nowrap rounded-lg transition-colors ${
              activeTab === item.key
                ? "bg-emerald-500 text-black font-bold"
                : "text-slate-400 hover:text-white"
            }`}
          >
            {item.icon}
            <span>{item.label}</span>
          </button>
        ))}
      </div>
    </header>
  );
};
