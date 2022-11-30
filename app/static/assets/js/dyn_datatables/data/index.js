export let myData = {}
export let modelName = ''

export const setData = (headings , data) => {
    myData = {
        headings: headings,
        data: data,
    }
}

export const setModelName = (data) => {
    modelName = data
}