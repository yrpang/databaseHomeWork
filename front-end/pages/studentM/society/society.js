// pages/studentM/society/society.js
const app = getApp()
Page({
  data: {
    checked: []
  },

  onLoad: function (options) {
    var info = JSON.parse(options.info)
    this.data.id = info['id']

    wx.request({
      url: app.globalData.baseURL + 'student/' + info['id'],
      method: "GET",
      success: res => {
        console.log(res.data)
        wx.request({
          url: app.globalData.baseURL + 'society',
          method: "GET",
          success: res2 => {
            console.log(res2.data)
            this.setData({
              society: res2.data.data,
              checked: res.data.data.society
            })
          }
        })
      }
    })
  },

  onChange: function (e) {
    this.setData({
      checked: e.detail.value.map(Number)
    })
  },

  submit: function () {
    wx.request({
      url: app.globalData.baseURL + "student/society/" + this.data.id,
      method: "PUT",
      data: {
        societyNo: this.data.checked
      },
      success:res=>{
        console.log(res.data)
        if (res.data.errCode == 0) {
          wx.showModal({
            title: "成功",
            content: "修改完成",
            showCancel: false,
            success(res) {
              if (res.confirm) {
                wx.navigateBack()
              }
            }
          })
        } else {
          wx.showModal({
            title: "错误",
            content: res.data.status,
            showCancel: false
          })
        }
      }
    })
  }
})