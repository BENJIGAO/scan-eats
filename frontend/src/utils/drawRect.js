export const drawRect = (detections, ctx) => {
  detections.forEach(prediction => {
    const [x, y, width, height] = prediction['bbox']
    const text = prediction['class']
    if (text !== 'apple' && text !== 'banana') return

    const color = 'green'
    ctx.strokeStyle = color
    ctx.font = '28px Arial'
    ctx.fillStyle = color

    ctx.beginPath()
    ctx.lineWidth = '6'
    ctx.fillText(text, x, y - 10)
    ctx.rect(x, y, width, height)
    ctx.stroke()
  })
}