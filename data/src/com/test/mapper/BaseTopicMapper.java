package com.test.mapper;

import java.util.List;
import chiya.core.base.page.Page;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import com.test.entity.Reply;
;
import com.test.entity.User;
;

@Mapper
public interface BaseTopicMapper {

	/**
	 * 添加帖子
	 * 
	 * @param topic 帖子
	 * @return 受影响行数
	 */
	Integer insertTopic(Topic topic);

	/**
	 * 添加多个帖子
	 * 
	 * @param list 帖子列表
	 * @return 受影响行数
	 */
	Integer insertTopicList(@Param("list") List<Topic> list);

	/**
	 * 添加或更新帖子，根据唯一性索引
	 * 
	 * @param list 帖子列表
	 * @return 受影响行数
	 */
	Integer insertOrUpdateTopicByUnique(Topic topic);

	/**
	 * 添加或更新帖子，根据查询条件
	 * 
	 * @param saveTopic 添加的帖子对象
	 * @param conditionTopic 帖子条件对象
	 * @return 受影响行数
	 */
	Integer insertOrUpdateTopicByWhere(@Param("saveTopic") Topic saveTopic, @Param("conditionTopic") Topic conditionTopic);

	/**
	 * 条件添加帖子
	 * 
	 * @param saveTopic 添加的帖子对象
	 * @param conditionTopic 帖子条件对象
	 * @return 受影响行数
	 */
	Integer insertTopicByWhereOnlySave(@Param("saveTopic") Topic saveTopic, @Param("conditionTopic") Topic conditionTopic);

	/**
	 * 根据id真删帖子
	 * 
	 * @param id 帖子的id
	 * @return 受影响行数
	 */
	Integer deleteTopicById(Integer id);

	/**
	 * 根据id列表真删帖子
	 * 
	 * @param list 帖子的id列表
	 * @return 受影响行数
	 */
	Integer deleteTopicInId(List<Integer> list);

	/**
	 * 根据id和其他条件真删帖子
	 * 
	 * @param id 帖子的id
	 * @param topic 帖子条件对象
	 * @return 受影响行数
	 */
	Integer deleteTopicByIdAndWhere(@Param("id") Integer id, @Param("topic") Topic topic);

	/**
	 * 根据条件真删帖子
	 * 
	 * @param topic 帖子条件对象
	 * @return 受影响行数
	 */
	Integer deleteTopic(Topic topic);

	/**
	 * 根据id假删帖子
	 * 
	 * @param id 帖子的id
	 * @return 受影响行数
	 */
	Integer falseDeleteTopicById(Integer id);

	/**
	 * 根据id修改帖子
	 * 
	 * @param topic 要更新的帖子对象
	 * @return 受影响行数
	 */
	Integer updateTopicById(Topic topic);

	/**
	 * 根据id和不满足的条件更新帖子，查询条件不满足时更新对象
	 * 
	 * @param saveTopic 更新的帖子对象
	 * @param conditionTopic 不存在的帖子对象
	 * @return 受影响行数
	 */
	Integer updateTopicByNotRepeatWhere(@Param("saveTopic") Topic saveTopic, @Param("conditionTopic") Topic conditionTopic);

	/**
	 * 根据id和其他的条件更新帖子
	 * 
	 * @param saveTopic 更新的帖子对象
	 * @param conditionTopic 帖子条件对象
	 * @return 受影响行数
	 */
	Integer updateTopicByIdAndWhere(@Param("saveTopic") Topic saveTopic, @Param("conditionTopic") Topic conditionTopic);

	/**
	 * 根据条件更新帖子
	 * 
	 * @param saveTopic 更新的帖子对象
	 * @param conditionTopic 条件帖子对象
	 * @return 受影响行数
	 */
	Integer updateTopic(@Param("saveTopic") Topic saveTopic, @Param("conditionTopic") Topic conditionTopic);

	/**
	 * 记录id设置其他字段为null
	 * 
	 * @param topic 设置成null的帖子对象，对象中字段不为Null则是要设置成null的字段
	 * @return 受影响行数
	 */
	Integer updateTopicSetNullById(Topic topic);

	/**
	 * 根据id查询帖子
	 * 
	 * @param id 帖子的id
	 * @return 帖子对象
	 */
	Topic selectTopicById(Integer id);

	/**
	 * 根据id列表查询帖子
	 * 
	 * @param list 帖子的id列表
	 * @return 帖子对象列表
	 */
	List<Topic> selectTopicInId(List<Integer> list);

	/**
	 * 只查询一个帖子
	 * 
	 * @param topic 帖子对象
	 * @param index 获取的下标值
	 * @return 帖子对象
	 */
	Topic selectOneTopic(@Param("topic")Topic topic, @Param("index")Integer index);

	/**
	 * 查询多个帖子
	 * 
	 * @param topic 帖子对象
	 * @param page 分页对象
	 * @return 帖子对象列表
	 */
	List<Topic> selectTopic(@Param("topic")Topic topic, @Param("page") Page page);

	/**
	 * 统计帖子记录数
	 * 
	 * @param topic 帖子对象
	 * @return 查询到的记录数
	 */
	Integer countTopic(@Param("topic")Topic topic);

	/**
	 * 内联一对一查询用户表
	 * 
	 * @param topic 帖子对象
	 * @param user 用户表对象
	 * @param page 分页对象
	 * @return 帖子对象列表
	 */
	List<Topic> findTopicOneToOneUser(@Param("topic") Topic topic, @Param("user") User user, @Param("page") Page page);

	/**
	 * 内联一对一统计用户表
	 * 
	 * @param topic 帖子对象
	 * @param user 用户表对象
	 * @return 查询到的记录数
	 */
	Integer countFindTopicOneToOneUser(@Param("topic") Topic topic, @Param("user") User user);

	/**
	 * 内联一对一查询用户表，只返回用户表
	 * 
	 * @param topic 帖子对象
	 * @param user 用户表对象
	 * @param page 分页对象
	 * @return 查询到的记录数
	 */
	List<User> linkOneToOneUser(@Param("topic") Topic topic, @Param("user") User user, @Param("page") Page page);

	/**
	 * 一对一查询用户表，只返回用户表
	 * 
	 * @param topic 帖子对象
	 * @param user 用户表对象
	 * @param page 分页对象
	 * @return 查询到的记录数
	 */
	List<Topic> queryTopicOneToOneUser(@Param("topic") Topic topic, @Param("user") User user, @Param("page") Page page);

	/**
	 * 内联一对多查询回复内容，双方均可分页
	 * 
	 * @param topic 帖子对象
	 * @param reply 回复内容对象
	 * @param onePage 帖子分页对象
	 * @param manyPage 回复内容分页对象
	 * @return 帖子对象列表
	 */
	List<Topic> findTopicOneToManyReply(@Param("topic") Topic topic, @Param("reply") Reply reply, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

	/**
	 * 内联一对多统计回复内容，双方均可分页
	 * 
	 * @param topic 帖子对象
	 * @param reply 回复内容对象
	 * @param onePage 帖子分页对象
	 * @param manyPage 回复内容分页对象
	 * @return 查询到的记录数
	 */
	Integer countFindTopicOneToManyReply(@Param("topic") Topic topic, @Param("reply") Reply reply, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

	/**
	 * 内联一对多查询回复内容，只返回回复内容
	 * 
	 * @param topic 帖子对象
	 * @param reply 回复内容对象
	 * @param onePage 帖子分页对象
	 * @param manyPage 回复内容分页对象
	 * @return 帖子对象列表
	 */
	List<Reply> linkOneToManyReply(@Param("topic") Topic topic, @Param("reply") Reply reply, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

	/**
	 * 外联一对多查询回复内容，双方均可分页
	 * 
	 * @param topic 帖子对象
	 * @param reply 回复内容对象
	 * @param onePage 帖子分页对象
	 * @param manyPage 回复内容分页对象
	 * @return 帖子对象列表
	 */
	List<Topic> queryTopicOneToManyReply(@Param("topic") Topic topic, @Param("reply") Reply reply, @Param("onePage") Page onePage, @Param("manyPage") Page manyPage);

}