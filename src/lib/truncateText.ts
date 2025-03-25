export const truncateText = (text: string, limit: number) => {
  if (text) {
    return text.length > limit ? `${text.slice(0, limit)}...` : text
  }
  return ''
}
