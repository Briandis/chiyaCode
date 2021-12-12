package com.test.entity;

import com.alibaba.fastjson.JSON;
import java.util.Date;
import java.util.List;
import com.test.entity.User;
import com.test.entity.Reply;

@SuppressWarnings("unchecked")
public abstract class BaseTopic<T> {

	/**
	 * 主键
	 * 
	 */
	private Integer id;
	/**
	 * 标题
	 * 
	 */
	private String title;
	/**
	 * 内容
	 * 
	 */
	private String data;
	/**
	 * 用户id
	 * 
	 */
	private Integer userId;
	/**
	 * 发布时间
	 * 
	 */
	private Date createTime;
	/**
	 * 修改时间
	 * 
	 */
	private Date updateTime;
	/**
	 * 删除标记
	 * 
	 */
	private Integer deleteFlag;
	/**
	 * 最大楼层
	 * 
	 */
	private Integer maxCount;
	/**
	 * 用户表
	 * 
	 */
	private User user;
	/**
	 * 回复内容
	 * 
	 */
	private List<Reply> listReply;

	/**
	 * 获取主键
	 * 
	 * @return 主键
	 */
	public Integer getId() {
		return id;
	}

	/**
	 * 获取标题
	 * 
	 * @return 标题
	 */
	public String getTitle() {
		return title;
	}

	/**
	 * 获取内容
	 * 
	 * @return 内容
	 */
	public String getData() {
		return data;
	}

	/**
	 * 获取用户id
	 * 
	 * @return 用户id
	 */
	public Integer getUserId() {
		return userId;
	}

	/**
	 * 获取发布时间
	 * 
	 * @return 发布时间
	 */
	public Date getCreateTime() {
		return createTime;
	}

	/**
	 * 获取修改时间
	 * 
	 * @return 修改时间
	 */
	public Date getUpdateTime() {
		return updateTime;
	}

	/**
	 * 获取删除标记
	 * 
	 * @return 删除标记
	 */
	public Integer getDeleteFlag() {
		return deleteFlag;
	}

	/**
	 * 获取最大楼层
	 * 
	 * @return 最大楼层
	 */
	public Integer getMaxCount() {
		return maxCount;
	}

	/**
	 * 获取用户表
	 * 
	 * @return 用户表
	 */
	public User getUser() {
		return user;
	}

	/**
	 * 获取回复内容
	 * 
	 * @return 回复内容
	 */
	public List<Reply> getListReply() {
		return listReply;
	}

	/**
	 * 设置主键
	 * 
	 * @param id 主键对象
	 */
	public void setId(Integer id) {
		this.id = id;
	}

	/**
	 * 设置标题
	 * 
	 * @param title 标题对象
	 */
	public void setTitle(String title) {
		this.title = title;
	}

	/**
	 * 设置内容
	 * 
	 * @param data 内容对象
	 */
	public void setData(String data) {
		this.data = data;
	}

	/**
	 * 设置用户id
	 * 
	 * @param userId 用户id对象
	 */
	public void setUserId(Integer userId) {
		this.userId = userId;
	}

	/**
	 * 设置发布时间
	 * 
	 * @param createTime 发布时间对象
	 */
	public void setCreateTime(Date createTime) {
		this.createTime = createTime;
	}

	/**
	 * 设置修改时间
	 * 
	 * @param updateTime 修改时间对象
	 */
	public void setUpdateTime(Date updateTime) {
		this.updateTime = updateTime;
	}

	/**
	 * 设置删除标记
	 * 
	 * @param deleteFlag 删除标记对象
	 */
	public void setDeleteFlag(Integer deleteFlag) {
		this.deleteFlag = deleteFlag;
	}

	/**
	 * 设置最大楼层
	 * 
	 * @param maxCount 最大楼层对象
	 */
	public void setMaxCount(Integer maxCount) {
		this.maxCount = maxCount;
	}

	/**
	 * 设置用户表
	 * 
	 * @param user 用户表对象
	 */
	public void setUser(User user) {
		this.user = user;
	}

	/**
	 * 设置回复内容
	 * 
	 * @param listReply 回复内容对象
	 */
	public void setListReply(List<Reply> listReply) {
		this.listReply = listReply;
	}


	/**
	 * 链式添加主键
	 * 
	 * @param id 主键对象
	 * @return 对象本身
	 */
	public T chainId(Integer id) {
		this.id = id;
		return (T) this;
	}

	/**
	 * 链式添加标题
	 * 
	 * @param title 标题对象
	 * @return 对象本身
	 */
	public T chainTitle(String title) {
		this.title = title;
		return (T) this;
	}

	/**
	 * 链式添加内容
	 * 
	 * @param data 内容对象
	 * @return 对象本身
	 */
	public T chainData(String data) {
		this.data = data;
		return (T) this;
	}

	/**
	 * 链式添加用户id
	 * 
	 * @param userId 用户id对象
	 * @return 对象本身
	 */
	public T chainUserId(Integer userId) {
		this.userId = userId;
		return (T) this;
	}

	/**
	 * 链式添加发布时间
	 * 
	 * @param createTime 发布时间对象
	 * @return 对象本身
	 */
	public T chainCreateTime(Date createTime) {
		this.createTime = createTime;
		return (T) this;
	}

	/**
	 * 链式添加修改时间
	 * 
	 * @param updateTime 修改时间对象
	 * @return 对象本身
	 */
	public T chainUpdateTime(Date updateTime) {
		this.updateTime = updateTime;
		return (T) this;
	}

	/**
	 * 链式添加删除标记
	 * 
	 * @param deleteFlag 删除标记对象
	 * @return 对象本身
	 */
	public T chainDeleteFlag(Integer deleteFlag) {
		this.deleteFlag = deleteFlag;
		return (T) this;
	}

	/**
	 * 链式添加最大楼层
	 * 
	 * @param maxCount 最大楼层对象
	 * @return 对象本身
	 */
	public T chainMaxCount(Integer maxCount) {
		this.maxCount = maxCount;
		return (T) this;
	}

	/**
	 * 链式添加用户表
	 * 
	 * @param user 用户表对象
	 * @return 对象本身
	 */
	public T chainUser(User user) {
		this.user = user;
		return (T) this;
	}

	/**
	 * 链式添加回复内容
	 * 
	 * @param listReply 回复内容对象
	 * @return 对象本身
	 */
	public T chainListReply(List<Reply> listReply) {
		this.listReply = listReply;
		return (T) this;
	}


	@Override
	public String toString() {
		return JSON.toJSONString(this);
	}

}