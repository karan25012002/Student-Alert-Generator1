/**
 * Safely render data to prevent React "Objects are not valid as a React child" errors
 */

export const safeString = (value, fallback = 'N/A') => {
  if (value === null || value === undefined) {
    return fallback
  }
  
  if (typeof value === 'string') {
    return value
  }
  
  if (typeof value === 'number' || typeof value === 'boolean') {
    return String(value)
  }
  
  if (typeof value === 'object') {
    try {
      return JSON.stringify(value)
    } catch (error) {
      return fallback
    }
  }
  
  return String(value)
}

export const safeNumber = (value, fallback = 0) => {
  const num = Number(value)
  return isNaN(num) ? fallback : num
}

export const safeArray = (value, fallback = []) => {
  return Array.isArray(value) ? value : fallback
}

export const safeObject = (value, fallback = {}) => {
  return value && typeof value === 'object' && !Array.isArray(value) ? value : fallback
}

export const safeRenderList = (items, renderFunction, fallback = null) => {
  if (!Array.isArray(items) || items.length === 0) {
    return fallback
  }
  
  try {
    return items.map((item, index) => {
      try {
        return renderFunction(item, index)
      } catch (error) {
        console.warn('Error rendering list item:', error, item)
        return null
      }
    }).filter(Boolean)
  } catch (error) {
    console.warn('Error rendering list:', error)
    return fallback
  }
}
