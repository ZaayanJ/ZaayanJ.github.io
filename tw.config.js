module.exports = {
  content: ['./index.html'],
  theme: { extend: {
    fontFamily: {
      display: ['"Chakra Petch"','sans-serif'],
      ui: ['"Plus Jakarta Sans"','system-ui','sans-serif'],
      sigil: ['UnifrakturMaguntia','Georgia','serif'],
      sans: ['Inter','system-ui','sans-serif'],
      mono: ['"JetBrains Mono"','ui-monospace','SFMono-Regular','monospace']
    },
    colors: { ink:'#06070A', well:'#020305', raise:'#0D0F14', hair:'rgba(200,208,222,0.15)',
              cy:'#D9DEE8', eb:'#8C1C34', fg:'#F2F4F8', mut:'#8A8F9C', ok:'#F2F5FA', ver:'#34D399' }
  }}
};
