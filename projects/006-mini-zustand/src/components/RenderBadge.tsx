import { useRef } from 'react'

export function RenderBadge() {
  const renders = useRef(0)
  // This diagnostic intentionally counts render attempts rather than committed effects.
  // eslint-disable-next-line react-hooks/refs
  renders.current += 1
  // eslint-disable-next-line react-hooks/refs
  return <span className="render-badge" title="Development render count">renders: {renders.current}</span>
}
