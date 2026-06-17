import re

with open("src/pages/History.jsx", "r", encoding="utf-8") as f:
    text = f.read()

# Top level div
text = text.replace("min-h-screen bg-gray-50", "min-h-screen text-gray-100")
text = text.replace("text-gray-900", "text-white")
text = text.replace("text-slate-900", "text-white")
text = text.replace("text-gray-500", "text-emerald-100/70")
text = text.replace("text-slate-500", "text-emerald-100/70")
text = text.replace("text-gray-400", "text-emerald-100/60")
text = text.replace("text-slate-400", "text-emerald-100/60")
text = text.replace("text-gray-200", "text-gray-300")
text = text.replace("text-gray-600", "text-gray-300")
text = text.replace("text-slate-600", "text-gray-300")

# Card backgrounds to glass-panel
text = text.replace("bg-white p-12 rounded-2xl shadow-sm text-center border border-gray-100", "glass-panel p-12 text-center text-white")
text = text.replace("bg-white px-4 py-2 rounded-lg shadow-sm text-sm text-gray-500 border border-gray-100", "glass-panel px-4 py-2 !rounded-lg text-sm text-gray-300 shadow-none")
text = text.replace("bg-white rounded-2xl shadow-sm overflow-hidden border border-gray-100", "glass-panel overflow-hidden border-white/20")
text = text.replace("bg-gray-100", "bg-black/30")

text = text.replace("bg-white/90 backdrop-blur-md px-8 py-5 border-b border-gray-100 flex justify-between items-center z-10", "bg-black/40 backdrop-blur-xl px-8 py-5 border-b border-white/10 flex justify-between items-center z-10")
text = text.replace("bg-white rounded-3xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-y-auto", "bg-black/60 backdrop-blur-3xl border border-white/20 rounded-3xl shadow-[0_0_40px_rgba(0,0,0,0.8)] max-w-3xl w-full max-h-[90vh] overflow-y-auto")
text = text.replace("p-2 hover:bg-gray-100 rounded-full transition-colors", "p-2 hover:bg-white/10 rounded-full transition-colors")

# Specific modal empty state
text = text.replace("bg-gray-50 border-2 border-dashed border-gray-200 rounded-2xl p-6", "glass-panel bg-black/20 border-2 border-dashed border-white/10 p-6")

# Knowledge base details
text = text.replace("p-4 bg-white rounded-2xl shadow-sm border-2 border-slate-200", "glass-panel p-4")
text = text.replace("p-4 bg-red-50 rounded-2xl shadow-sm border-2 border-red-200", "glass-panel bg-red-500/10 p-4 border-red-400/30")
text = text.replace("p-4 bg-amber-50 rounded-2xl shadow-sm border-2 border-amber-200", "glass-panel bg-amber-500/10 p-4 border-amber-400/30")

text = text.replace("p-5 bg-red-100 rounded-2xl shadow-inner border-2 border-red-300", "glass-panel bg-red-500/20 p-5 border-red-400/50 shadow-[0_0_15px_rgba(248,113,113,0.2)]")
text = text.replace("p-5 bg-emerald-50 rounded-2xl shadow-sm border-2 border-emerald-200", "glass-panel bg-emerald-500/10 p-5 border-emerald-400/30")

text = text.replace("p-4 bg-indigo-50 rounded-2xl shadow-sm border-2 border-indigo-200", "glass-panel bg-indigo-500/10 p-4 border-indigo-400/30")

text = text.replace("bg-gray-50 p-4 rounded-xl border border-gray-100", "glass-panel bg-black/20 p-4 shadow-none border-white/10")
text = text.replace("bg-red-50 border-red-100", "bg-red-500/20 border-red-400/30 text-red-100")
text = text.replace("bg-amber-50 border-amber-100", "bg-amber-500/20 border-amber-400/30 text-amber-100")
text = text.replace("bg-green-50 border-green-100", "bg-emerald-500/20 border-emerald-400/30 text-emerald-100")

text = text.replace("bg-gray-50 p-2 rounded-lg", "bg-white/10 p-2 rounded-lg border border-white/5")

# Interactive cards text
text = text.replace("text-emerald-900", "text-emerald-300 drop-shadow-md")
text = text.replace("text-red-900", "text-red-300 drop-shadow-md")

# InteractiveCard inner logic
text = text.replace("!bg-white'", "!bg-white/20 !border-white/40 !shadow-[0_0_20px_rgba(255,255,255,0.2)]'")
text = text.replace("hover:shadow-md", "hover:bg-white/10")
text = text.replace("text-[#222]", "text-white")

with open("src/pages/History.jsx", "w", encoding="utf-8") as f:
    f.write(text)

print("History updated successfully")
