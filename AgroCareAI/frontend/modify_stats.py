import re

with open("src/pages/Stats.jsx", "r", encoding="utf-8") as f:
    text = f.read()

# Tooltip
text = text.replace('className="bg-[#1a241d] border border-[#2a3b30] p-3 rounded-lg shadow-xl shadow-black/50 text-xs text-gray-200"', 'className="glass-panel bg-black/60 p-3 text-xs text-gray-200 shadow-none border-white/20"')

# Error Box
text = text.replace('className="p-8 rounded-2xl border text-center"', 'className="glass-panel p-8 text-center"')

# Loading states & general removal of style={{ ... }}
text = text.replace(' style={{ backgroundColor: THEME.bgMain }}', '')
text = text.replace(' style={{ backgroundColor: THEME.bgCard, borderColor: THEME.border }}', '')

# Top level div
text = text.replace('className="min-h-screen flex items-center justify-center p-4"', 'className="min-h-screen text-gray-100 flex items-center justify-center p-4"')
text = text.replace('className="flex justify-center items-center h-screen"', 'className="flex justify-center items-center h-screen text-gray-100"')
text = text.replace('className="min-h-screen pb-16 pt-8 px-4 sm:px-6 lg:px-8 font-sans selection:bg-[#a3e635] selection:text-black"', 'className="min-h-screen text-gray-100 pb-16 pt-8 px-4 sm:px-6 lg:px-8 font-sans selection:bg-[#a3e635] selection:text-black"')

# Card Replacements
text = text.replace('className="p-6 rounded-2xl border flex flex-col justify-between relative overflow-hidden"', 'className="glass-panel p-6 flex flex-col justify-between relative overflow-hidden shadow-[0_0_20px_rgba(0,0,0,0.5)]"')
text = text.replace('className="p-6 rounded-2xl border lg:col-span-1 relative flex flex-col items-center justify-center"', 'className="glass-panel p-6 lg:col-span-1 relative flex flex-col items-center justify-center shadow-[0_0_20px_rgba(0,0,0,0.5)]"')
text = text.replace('className="p-6 rounded-2xl border flex flex-col"', 'className="glass-panel p-6 flex flex-col shadow-[0_0_20px_rgba(0,0,0,0.5)]"')
text = text.replace('className="p-6 rounded-2xl border"', 'className="glass-panel p-6 shadow-[0_0_20px_rgba(0,0,0,0.5)]"')

# Glow effect correction
text = text.replace('bg-[#a3e635] opacity-5', 'bg-emerald-400 opacity-20')
text = text.replace('from-[#a3e635] to-transparent opacity-50', 'from-emerald-400 to-transparent opacity-30')

with open("src/pages/Stats.jsx", "w", encoding="utf-8") as f:
    f.write(text)

print("Stats updated successfully")
