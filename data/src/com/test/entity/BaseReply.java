package com.test.entity;

import com.alibaba.fastjson.JSON;
import java.util.Date;
import com.test.entity.User;
import com.test.entity.Topic;

@SuppressWarnings("unchecked")
public abstract class BaseReply<T> {

	/**
	 * 主键
	 * 
	 */
	private Integer id;
	/**
	 * 帖子id
	 * 
	 */
	private Integer topicId;
	/**
	 * 用户id
	 * 
	 */
	private Integer userId;
	/**
	 * 回复内容
	 * 
	 */
	private String data;
	/**
	 * 创建时间
	 * 
	 */
	private Date createTime;
	/**
	 * 删除标记
	 * 
	 */
	private Integer deleteFlag;
	/**
	 * 帖子
	 * 
	 */
	private Topic topic;
	/**
	 * 用户表
	 * 
	 */
	private User user;

	/**
	 * 获取主键
	 * 
	 * @return 主键
	 */
	public Integer getId() {
		return id;
	}

	/**
	 * 获取帖子id
	 * 
	 * @return 帖子id
	 */
	public Integer getTopicId() {
		return topicId;
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
	 * 获取回复内容
	 * 
	 * @return 回复内容
	 */
	public String getData() {
		return data;
	}

	/**
	 * 获取创建时间
	 * 
	 * @return 创建时间
	 */
	public Date getCreateTime() {
		return createTime;
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
	 * 获取帖子
	 * 
	 * @return 帖子
	 */
	public Topic getTopic() {
		return topic;
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
	 * 设置主键
	 * 
	 * @param id 主键对象
	 */
	public void setId(Integer id) {
		this.id = id;
	}

	/**
	 * 设置帖子id
	 * 
	 * @param topicId 帖子id对象
	 */
	public void setTopicId(Integer topicId) {
		this.topicId = topicId;
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
	 * 设置回复内容
	 * 
	 * @param data 回复内容对象
	 */
	public void setData(String data) {
		this.data = data;
	}

	/**
	 * 设置创建时间
	 * 
	 * @param createTime 创建时间对象
	 */
	public void setCreateTime(Date createTime) {
		this.createTime = createTime;
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
	 * 设置帖子
	 * 
	 * @param topic 帖子对象
	 */
	public void setTopic(Topic topic) {
		this.topic = topic;
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
	 * 链式添加帖子id
	 * 
	 * @param topicId 帖子id对象
	 * @return 对象本身
	 */
	public T chainTopicId(Integer topicId) {
		this.topicId = topicId;
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
	 * 链式添加回复内容
	 * 
	 * @param data 回复内容对象
	 * @return 对象本身
	 */
	public T chainData(String data) {
		this.data = data;
		return (T) this;
	}

	/**
	 * 链式添加创建时间
	 * 
	 * @param createTime 创建时间对象
	 * @return 对象本身
	 */
	public T chainCreateTime(Date createTime) {
		this.createTime = createTime;
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
	 * 链式添加帖子
	 * 
	 * @param topic 帖子对象
	 * @return 对象本身
	 */
	public T chainTopic(Topic topic) {
		this.topic = topic;
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


	@Override
	public String toString() {
		return JSON.toJSONString(this);
	}

}