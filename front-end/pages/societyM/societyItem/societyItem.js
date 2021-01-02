// pages/departmentM/departmentItem/departmentItem.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    ifnew: false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.data.id = options.id
    if (options.id == -1) {
      this.setData({
        data: {
          societyName: "",
          societyYear: "",
          societyLoc: ""
        },
        ifnew: true
      })
      return
    }
    wx.request({
      url: app.globalData.baseURL + 'society/' + options.id,
      method: "GET",
      success: res => {
        console.log(res.data),
          this.setData({
            data: res.data.data
          })
      }
    })
  },

  nameInput: function (e) {
    this.setData({
      ["data.societyName"]: e.detail.value
    })
  },

  yearInput: function (e) {
    this.setData({
      ["data.societyYear"]: e.detail.value
    })
  },

  locInput: function (e) {
    this.setData({
      ["data.societyLoc"]: e.detail.value
    })
  },

  submit: function () {
    if (!this.data.data.societyName || !this.data.data.societyYear || !this.data.data.societyLoc) {
      this.setData({
        error: "所有字段不能为空"
      })
      return
    }
    wx.request({
      url: app.globalData.baseURL + 'society/' + this.data.id,
      method: "PUT",
      data: {
        societyName: this.data.data.societyName,
        societyYear: this.data.data.societyYear,
        societyLoc: this.data.data.societyLoc
      },
      success: res => {
        console.log(res)
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
            showCancel: false,
          })
        }
        if (res.statusCode != 200) {
          wx.showModal({
            title: "错误",
            content: "请检查字段约束",
            showCancel: false,
          })
        }
      }
    })
  },

  create: function () {
    if (!this.data.data.societyName || !this.data.data.societyYear || !this.data.data.societyLoc) {
      this.setData({
        error: "所有字段不能为空"
      })
      return
    }
    wx.request({
      url: app.globalData.baseURL + 'society',
      method: "POST",
      data: {
        societyName: this.data.data.societyName,
        societyYear: this.data.data.societyYear,
        societyLoc: this.data.data.societyLoc
      },
      success: res => {
        console.log(res)
        if (res.data.errCode == 0) {
          wx.showModal({
            title: "成功",
            content: "添加完成",
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
            showCancel: false,
          })
        }
        // Todo: 需要修改完善
        if (res.statusCode != 200) {
          wx.showModal({
            title: "错误",
            content: "请检查字段约束",
            showCancel: false,
          })
        }
      }
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})