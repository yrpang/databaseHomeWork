// pages/changeClassNo/changeClassNo.js
const app = getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    wx.request({
      url: app.globalData.baseURL + 'class',
      method: "GET",
      success: res => {
        console.log(res.data)
        this.setData({
          data: {
            classIndex: -1
          },
          classes: res.data.data
        })
      }
    })

  },

  bindChange: function (e) {
    console.log(e)
    this.setData({
      classIndex: e.detail.value,
      ["data.classNo"]: this.data.classes[e.detail.value]['classNo']
    })
  },

  newInput: function (e) {
    this.setData({
      ["newNo"]: e.detail.value
    })
  },

  submit: function () {
    if (!this.data.data.classNo || !this.data.newNo) {
      this.setData({
        error: "所有字段不能为空"
      })
      return
    }
    wx.request({
      url: app.globalData.baseURL + 'manage/changeClassNo',
      method: 'POST',
      data: {
        old_No: String(this.data.data.classNo),
        new_No: String(this.data.newNo)
      },
      success: res=>{
        console.log(res)
        if (res.data.errCode == 0) {
          wx.showModal({
            title: "成功",
            content: "新班级人数:"+res.data.data,
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
            success(res) {
            }
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